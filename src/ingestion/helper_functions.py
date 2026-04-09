import pandas as pd
import time
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}

def chunk_dataframe(df, size=500):
    for start in range(0, len(df), size):
        yield df.iloc[start:start + size]

def get_winner(f1, f2, fighters):
    status1 = fighters[0].select_one(".b-fight-details__person-status")
    status2 = fighters[1].select_one(".b-fight-details__person-status")
    status1_text = status1.get_text(strip=True).upper() if status1 else ""
    status2_text = status2.get_text(strip=True).upper() if status2 else ""
    if status1_text == "W":
        return f1
    elif status2_text == "W":
        return f2
    else:
        return "No Contest"

def get_info(label, soup):
    for p in soup.select("p.b-fight-details__text"):
        for tag in p.find_all("i", class_="b-fight-details__label"):
            if tag.get_text(strip=True) == label:
                next_node = tag.next_sibling
                while next_node:
                    if isinstance(next_node, str):
                        text = next_node.strip()
                        if text:
                            return text
                    elif hasattr(next_node, "get_text"):
                        text = next_node.get_text(strip=True)
                        if text:
                            return text
                    next_node = next_node.next_sibling
    return None

def get_event_name(soup):
    header = soup.select_one("h2.b-content__title")
    if header:
        return header.get_text(strip=True).replace("Event:", "").strip()
    return None

def get_result_details(soup):
    paragraphs = soup.select("p.b-fight-details__text")
    for p in paragraphs:
        if "Details:" in p.text:
            text = p.get_text(separator=" ", strip=True)
            if "Details:" in text:
                return text.split("Details:")[-1].strip()
    return None

def get_fighter_id(soup, stats, fighter):
    try:
        return stats[0].text.strip() if fighter == 1 else stats[1].text.strip()
    except:
        return soup.select(
            "a.b-fight-details__person-link"
        )[fighter - 1].get_text(strip=True)

def get_striking_stats(stats, fighter):
    i = 0 if fighter == 1 else 1
    try:
        return (
            stats[2 + i].text.strip(),                         # knockdowns
            stats[8 + i].text.split(" of ")[1].strip(),        # total att
            stats[8 + i].text.split(" of ")[0].strip(),        # total succ
            stats[4 + i].text.split(" of ")[1].strip(),        # sig att
            stats[4 + i].text.split(" of ")[0].strip(),        # sig succ
        )
    except:
        return (None, None, None, None, None)

def get_grappling_stats(stats, fighter):
    i = 0 if fighter == 1 else 1
    try:
        return (
            stats[10 + i].text.split(" of ")[1].strip(),  # TD att
            stats[10 + i].text.split(" of ")[0].strip(),  # TD succ
            stats[14 + i].text.strip(),                   # SUB att
            stats[16 + i].text.strip(),                   # REV
            stats[18 + i].text.strip(),                   # CTRL
        )
    except:
        return (None, None, None, None, None)


def get_fighter_urls():
    pass
def get_latest_event():
    logging.info("🔎 Fetching latest UFC event...")
    try:
        response = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        event_link = soup.select_one('i.b-statistics__table-content a.b-link[href*="event-details"]')

        if not event_link:
            logging.warning("⚠️ No events found.")
            return None
            
        return {
            'url': event_link['href'].strip(),
            'name': event_link.text.strip()
        }

    except Exception as e:
        logging.error(f"❌ Error while fetching event: {str(e)}")
        return None
    
def get_event_details(event_url):
    try:
        response = requests.get(event_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        event_name = soup.find('h2', class_='b-content__title').get_text(strip=True)
        
        details_section = soup.find('div', class_='b-list__info-box')
        date_str = location_str = 'N/A'

        if details_section:
            for item in details_section.find_all('li'):
                text = item.get_text(strip=True)
                if 'Date:' in text: date_str = text.split('Date:')[-1].strip()
                if 'Location:' in text: location_str = text.split('Location:')[-1].strip()

        try:
            event_date = datetime.strptime(date_str, '%B %d, %Y').strftime('%Y-%m-%d')
        except Exception:
            event_date = date_str

        location_parts = [part.strip() for part in location_str.split(',')]
        fight_rows = soup.select('tr.b-fight-details__table-row')[1:]
        fights = []

        for row in fight_rows:
            fighters = row.select('a.b-link_style_black')

            fight_data = {
                'event_name': event_name,
                'event_date': event_date,
                'event_city': location_parts[0] if location_parts else None,
                'event_state': location_parts[1] if len(location_parts) > 1 else None,
                'event_country': location_parts[-1] if location_parts else None,
                'fighter1_name': fighters[0].text.strip() if len(fighters) > 0 else 'N/A',
                'fighter1_link': fighters[0]['href'] if len(fighters) > 0 else 'N/A',
                'fighter2_name': fighters[1].text.strip() if len(fighters) > 1 else 'N/A',
                'fighter2_link': fighters[1]['href'] if len(fighters) > 1 else 'N/A',
                'weight_class': row.select_one('td:nth-of-type(7) p').get_text(strip=True) 
                                if row.select_one('td:nth-of-type(7) p') else 'N/A',
            }

            fights.append(fight_data)

        return fights

    except Exception as e:
        logging.error(f"❌ Error parsing event details: {str(e)}")
        return []

# Parsers
def parse_int(val):
    try:
        if val is None:
            return None
        val = str(val).strip()
        if val in ("", "--"):
            return None
        return int(float(val))
    except:
        return None

def parse_l_name(name): return name[-1] if len(name) == 2 else (
    'NULL' if len(name) <= 1 else ' '.join(name[-(len(name)-1):-0]))
def parse_nickname(n): return n.strip() if n != '\n' else 'NULL'
def parse_height(h): return None if '--' in h else int((int(h[0])*12 + int(h.split("'")[1].strip().strip('"'))) * 2.54)
def parse_reach(r): return None if '--' in r else int(r.strip().strip('"')) * 2.54
def parse_weight(w): return None if '--' in w else int(w.split()[0].strip())
def parse_stance(s): return s.strip() if s.strip() else 'NULL'
def parse_dob(d): return None if d == '--' else datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d')



def scrape_one_fight(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        stats = soup.select("p.b-fight-details__table-text")

        rows = []

        for fighter in [1, 2]:
            fighter_id = get_fighter_id(soup, stats, fighter)

            k, tsa, tss, ssa, sss = get_striking_stats(stats, fighter)
            tda, tds, sa, rev, ctrl = get_grappling_stats(stats, fighter)

            rows.append({
                "fight_url": url.rstrip("/"),
                "fighter_id": fighter_id,
                "knockdowns": parse_int(k),
                "total_strikes_att": parse_int(tsa),
                "total_strikes_succ": parse_int(tss),
                "sig_strikes_att": parse_int(ssa),
                "sig_strikes_succ": parse_int(sss),
                "takedown_att": parse_int(tda),
                "takedown_succ": parse_int(tds),
                "submission_att": parse_int(sa),
                "reversals": parse_int(rev),
                "ctrl_time": ctrl,
            })

        return rows

    except Exception as e:
        logging.warning(f"❌ Failed to scrape {url}: {e}")
        return []


def scrape_fighter_from_url(url):

    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "lxml")
        
        name = soup.select_one('span')
        if not name:
            return None
        name_parts = name.get_text(strip=True).split()
        f_name = name_parts[0]
        l_name = parse_l_name(name_parts)
        
        nick = soup.select_one('p.b-content__Nickname')
        nickname = parse_nickname(nick.text) if nick else "NULL"

        details = soup.select('li.b-list__box-list-item')
        if len(details) < 5:
            return None
        
        height = parse_height(details[0].text.split(":")[1].strip())
        weight = parse_weight(details[1].text.split(":")[1].strip())
        reach = parse_reach(details[2].text.split(":")[1].strip())
        stance = parse_stance(details[3].text.split(":")[1].strip())
        dob = parse_dob(details[4].text.split(":")[1].strip())

        record = soup.select_one('span.b-content__title-record')
        if not record:
            return None
        rec = record.get_text(strip=True).split(":")[1].strip().split("-")
        w, l = int(rec[0]), int(rec[1])
        d = int(rec[-1][0]) if len(rec[-1]) > 1 else int(rec[-1])
        nc = int(rec[-1].split("(")[-1][0]) if '(' in rec[-1] else 0

        stats = soup.select('p.b-fight-details__table-text')

        stats = soup.select('ul.b-list__box-list.b-list__box-list_margin-top li.b-list__box-list-item')
        stats_dict = {}
        for stat in stats:
            try:
                k, v = stat.text.split(":")
                stats_dict[k.strip()] = v.strip()
            except: continue

        return {
            "fighter_f_name": f_name,
            "fighter_l_name": l_name,
            "fighter_nickname": nickname,
            "fighter_height_cm": height,
            "fighter_weight_lbs": weight,
            "fighter_reach_cm": reach,
            "fighter_stance": stance,
            "fighter_dob": dob,
            "fighter_w": w,
            "fighter_l": l,
            "fighter_d": d,
            "fighter_nc_dq": nc,
            "fighter_slpm": float(stats_dict.get("SLpM", 0)),
            "fighter_str_acc": float(stats_dict.get("Str. Acc.", "0").strip("%")) / 100,
            "fighter_sapm": float(stats_dict.get("SApM", 0)),
            "fighter_str_def": float(stats_dict.get("Str. Def", "0").strip("%")) / 100,
            "fighter_td_avg": float(stats_dict.get("TD Avg.", 0)),
            "fighter_td_acc": float(stats_dict.get("TD Acc.", "0").strip("%")) / 100,
            "fighter_td_def": float(stats_dict.get("TD Def.", "0").strip("%")) / 100,
            "fighter_sub_avg": float(stats_dict.get("Sub. Avg.", 0)),
            "fighter_url": url,
        }

        
        

        
    except Exception as e:
        logging.warning(f"❌ Failed to scrape {url}: {e}")
        return []



