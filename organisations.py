"""Master list of Chennai Margazhi-season Carnatic organisers, with 2026-27 status.

Only definite organisations / sabhas belong here. Concerts whose source names no organiser use
organisation = "Organiser not stated"; that label is NOT an organisation and is not listed.

Status values: "Schedule published", "Dates announced", "Awaiting 2026–27 schedule".
Writes data/organisations.json. Names for published organisers must match concerts.json.
"""
import json
from pathlib import Path

PUB, ANN, AW = "Schedule published", "Dates announced", "Awaiting 2026–27 schedule"
MAJOR, OTHER, FEST = "Major sabha", "Other sabha", "Festival / arts organisation"

# name, group, status, area, venue, 2026-27 festival + dates, note, url
ORGS = [
    ("The Music Academy, Madras", MAJOR, PUB, "Alwarpet / TTK Road", "Music Academy Auditorium, 168 TTK Road",
     "100th Annual Concerts · 15 Dec 2026 – 1 Jan 2027", "Conference sessions daily 8–10 am; dance festival 3–9 Jan 2027.",
     "https://musicacademymadras.in/100th-annual-concerts-2026/"),
    ("Bharat Kalachar", MAJOR, PUB, "T. Nagar", "Sri YGP Auditorium, 17 Thirumalai Road",
     "38th Marghazhi Mahotsav · 13 Dec 2026 – 17 Jan 2027", "Advance booking at venue from 7 Dec 2026.",
     "https://www.bharatkalachar.com/38-bharat-kalachar.html"),
    ("Kartik Fine Arts", MAJOR, PUB, "Alwarpet / TTK Road", "Narada Gana Sabha, TTK Road", "52nd Art Festival · 2–12 Dec 2026",
     "Two ticketed concerts a day (4 or 4.30 pm and 6.45 pm) at Narada Gana Sabha, 2–12 Dec, listed on MDnD; the dance programmes of 3, 6 and 11 Dec evenings are not listed here. S. J. Jananiy's 26 Dec concert at Bharatiya Vidya Bhavan comes from Bandsintown.",
     "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("Narada Gana Sabha", MAJOR, PUB, "Alwarpet / TTK Road", "TTK Road, Teynampet", "Isai Natya Nataka Vizha 2026 · 13 Dec 2026 – 1 Jan 2027",
     "Ticketed concerts at 3.30 pm and 6.30 pm (6 pm on some days), 13–31 Dec, on the sabha's MDnD page; dance, discourse and bhajan items (19, 22 and 31 Dec, 1 Jan) are not listed here. Season passes on MDnD (Members and All Season Pass 13 Dec – 1 Jan; Core Season Pass 20 Dec – 1 Jan).",
     "https://mdnd.in/SeasonTickets/OrganizerLandingPage?ci=101&r_id=2400"),
    ("Sri Krishna Gana Sabha", MAJOR, PUB, "T. Nagar", "Dr. Nalli Gana Vihar, 20 Maharajapuram Santhanam Salai",
     "70th Margazhi Mela · 12 Dec 2026 – 3 Jan 2027", "Music and dance; tickets on tikkl.com. Natya Kala Conference (dance) 26–28 Dec.",
     "https://krishnaganasabha.com/assets/images/nkc/margazhimela2026/MM_schedule(2026).pdf"),
    ("Sri Thyaga Brahma Gana Sabha", MAJOR, AW, "T. Nagar", "Vani Mahal, G.N. Road", "", "", "https://www.vanimahal.com/"),
    ("Brahma Gana Sabha", MAJOR, AW, "Mylapore", "Sivagami Pethachi Auditorium", "", "", ""),
    ("Mylapore Fine Arts Club", MAJOR, AW, "Mylapore", "45 Musiri Subramaniam Road", "", "", ""),
    ("Sri Parthasarathy Swami Sabha", MAJOR, PUB, "Mylapore", "Vidya Bharathi Kalyana Mandapam, Bheemasena Garden Road",
     "126th Year Isai Vizha · 17 Dec 2026 – 3 Jan 2027", "Two ticketed concerts daily, 4 pm and 6.30 pm, 17 Dec – 2 Jan, on the sabha's MDnD festival page (venue Vidya Bharathi Kalyana Mandapam); Shashank & Abhishek Raghuram 3 Jan from the artist's site.",
     "https://mdnd.in/SeasonTickets/OrganizerLandingPage?ci=101&r_id=2304"),
    ("The Indian Fine Arts Society", MAJOR, AW, "Alwarpet / TTK Road", "Ethiraja Kalyana Nilayam, TTK Road", "", "", ""),
    ("Rasika Ranjani Sabha", MAJOR, AW, "Mylapore", "Dakshinamoorthy Auditorium", "", "", "https://rrsabha.org/"),
    ("Bharatiya Vidya Bhavan, Chennai Kendra", MAJOR, AW, "Mylapore", "East Mada Street", "", "Its festival usually opens the season in late November.", "https://www.bhavanschennai.org/events_news.php"),
    ("Tamil Isai Sangam", MAJOR, AW, "George Town", "Rajah Annamalai Mandram, Esplanade Road", "", "", ""),
    ("Hamsadhwani", MAJOR, AW, "Adyar", "Indira Nagar", "Margazhi Maha Utsavam", "Sandeep Narayan's website lists a 9 Dec 2026 \"Margazhi Maha Utsavam\" concert at Hamsadhwani, Indira Nagar (organiser not named there).", ""),
    ("Asthika Samajam", MAJOR, AW, "Alwarpet", "Venus Colony", "", "", ""),
    ("Chromepet Cultural Academy", OTHER, AW, "Chromepet", "", "", "Margazhi Festival.", ""),
    ("Thrimoorthi Sangeetha Sabha", OTHER, AW, "", "", "", "", ""),
    ("Sri Krishna Fine Arts Society", OTHER, AW, "Nanganallur", "", "", "", ""),
    ("Meenakshi Sundararajan Fine Arts Academy", OTHER, AW, "", "", "", "", ""),
    ("Music Education Trust", OTHER, AW, "", "", "", "", ""),
    ("Shri Purandaradaasar Trust", OTHER, AW, "", "", "", "Music festival.", ""),
    ("Sampoornam Foundation for Music and Arts", FEST, AW, "Mylapore", "Arkay Convention Centre", "", "Margazhi Music Festival.", ""),
    ("Naadhabrahmam", FEST, AW, "Mylapore", "Srinivasa Sastri Hall, Luz", "", "Sangeetha Raga Mahothsavam.", ""),
    ("Trinity Arts", FEST, AW, "", "", "", "Trinity Arts Festival.", ""),
    ("Parampara", FEST, AW, "", "", "", "Ragasudharasa Music Festival series.", ""),
    ("Parivadini", FEST, AW, "", "", "", "Concert series, also recorded online.", ""),
    ("Maha Periyava Anusham Trust", FEST, AW, "Mylapore", "Mylai Maha-periyava Temple, Pichupillai Street", "", "Margazhi Sangeetha Upasana early-morning concerts, with Mani Mohanam Academy.", ""),
    ("SciArtsRUs", FEST, AW, "Mylapore", "Bharatiya Vidya Bhavan; P.S. High School; IIT Madras", "", "Margazhi Matram festival.", ""),
    ("Bharat Sangeet Utsav", FEST, ANN, "Alwarpet / TTK Road", "Narada Gana Sabha", "Bharat Sangeet Utsav 2026 · 31 Oct – 7 Nov 2026", "Presented by Carnatica with Sri Parthasarathy Swami Sabha at Narada Gana Sabha. Held before the 15 Nov – 31 Jan season window, so its concerts are not listed here.", "https://kalaverse.com/festivals/bharat-sangeet-utsav-2026"),
    ("Sruti Foundation & The Music Forum", FEST, AW, "Mylapore", "Bharatiya Vidya Bhavan Mini Hall", "", "LecDem Mela (lecture-demonstrations).", ""),
    ("Neelakanta Sivan Cultural Academy", OTHER, AW, "Sholinganallur", "", "", "Runs the Neelakanta Sivan School of Art and Culture. 2026–27 dates not yet found online.", ""),
    ("Kapali Fine Arts", OTHER, AW, "Mylapore", "", "", "", ""),
    ("Nungambakkam Cultural Academy", OTHER, AW, "Nungambakkam", "", "", "", ""),
    ("Kalarasana", OTHER, AW, "", "", "", "", ""),
    ("Nadopasana", OTHER, AW, "", "", "", "", ""),
    ("Sri Rama Bhaktha Jana Samaj", OTHER, AW, "", "", "", "", ""),
    ("Nandi Fine Arts", OTHER, AW, "", "", "", "", ""),
    ("Perambur Sangeetha Sabha", OTHER, AW, "Perambur", "", "", "", ""),
    ("Sat Sangam Sabha", OTHER, AW, "Madipakkam", "", "", "", ""),
    ("Chennai Cultural Academy Trust", OTHER, AW, "", "", "", "", ""),
    ("Naada Inbam", FEST, AW, "Mylapore", "Ragasudha Hall, Luz Avenue", "", "", ""),
    ("Charsur Arts Foundation", FEST, PUB, "Teynampet", "My Bungalow, 40 Eldams Road",
     "DVAYAM – Sounds of Duality · 15–31 Dec 2026", "Two concerts daily, 4 pm and 6.30 pm (plus some 10 am slots); programme for 15–30 Dec listed on MDnD, 31 Dec not yet listed. Lecture-demonstrations not included.",
     "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("Chennai Fine Arts", FEST, AW, "", "", "", "", ""),
    ("Madhuradhwani", FEST, AW, "Mylapore", "Arkay Convention Centre", "", "ACC Anniversary festival.", ""),
    ("Sunaadalahari", FEST, AW, "Abhiramapuram", "Indira Ranganathan Trust, 52 C.P. Ramaswamy Road", "", "Garden-setting concerts.", ""),
    ("Carnatica", FEST, AW, "Mylapore", "Desiga Vidya Bhavanam (Paddhathi Music Fest)", "", "Also runs the Global Heritage Music Fest. Co-presents Bharat Sangeet Utsav 2026 (31 Oct – 7 Nov, before the season) with Sri Parthasarathy Swami Sabha.", "https://carnatica.net/"),
    ("MDnD", FEST, AW, "Mylapore", "MDnD Performance Centre, Luz Church Road", "", "Anandha Margazhi; also sells season tickets for many sabhas. An \"Anandha Margazhi\" (Indian Stage) is listed for 12–26 Dec 2026; no programme yet.","https://www.mdnd.in/seasontickets"),
    ("Nada Sudha", FEST, AW, "Velachery", "Sri Ganapathy Sachchidananda Ashram", "", "", ""),
    ("Sruthi Laya Kendra", FEST, AW, "Mylapore", "Bharatiya Vidya Bhavan Mini Hall", "", "Winter Music Festival.", ""),
    ("Gayatri Fine Arts Global", FEST, AW, "Mylapore", "Sri Krishna Saras Hall, P.S. Sivaswamy Salai", "", "", ""),
    ("Shakthi Sangita Sabha", FEST, AW, "Valasaravakkam", "Anbu Nagar", "", "", ""),
    ("SASTRA Satsangh", FEST, AW, "", "", "", "Margazhi Mela.", ""),
    ("TTVV Trust & Cleveland Thyagaraja Festival", FEST, AW, "Teynampet", "Tattvaloka Hall, Eldams Road", "", "Margazhi Mela.", ""),
    ("VVS Foundation & SaMaa Arts", FEST, AW, "Mylapore", "Raghavendra Swami Mutt, Salai Street; Sri Srikara Anjaneya Raghavendra Swamy Sannidhanam, near R.R. Sabha", "Ekaantha Sangeetha Seva (early-morning concerts)", "Swagatham and Ekaantha Sangeetha Seva festivals.", ""),
    ("Kauvery Margazhi Maha Utsavam", FEST, AW, "", "", "", "Organiser name not found; listed under the festival name.", ""),
    ("Lalitha Jewellery", FEST, AW, "Valasaravakkam", "Jyothi Indira Thirumana Mandapam", "", "Runs the Jyothi Indira Margazhi Yuvautsav.", ""),
    ("Lakshman Sruthi", FEST, AW, "", "", "", "Runs the Chennaiyil Thiruvaiyaru festival.", ""),
    ("Chennaiyil Sangeeth Utsav", FEST, PUB, "Neelankarai", "AMRK Banquet Hall (earlier editions)", "Chennaiyil Sangeeth Utsav · 9–13 Jan 2027", "Four ticketed 6.30 pm concerts listed on MDnD (9, 10, 12, 13 Jan 2027); venue not printed for 2027. Organiser name not found; listed under the festival name.", "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("RASOHAM", FEST, ANN, "Alwarpet", "Rasoham, Alwarpet", "Kutty Kutchery Festival 2026 · 12–21 Dec 2026",
     "Ten-day festival listed on ragarasa.in (Carnatic vocal and instrumental, Hindustani, dance and folk); programme not yet published.",
     "https://rasoham.org/"),
    ("Medai The Stage", FEST, AW, "Alwarpet", "1st Cross St, Co-operative Colony", "", "", ""),
    ("Triplicane Music Festival", FEST, AW, "Triplicane", "NKT Muthu Hall", "", "Organiser name not found; listed under the festival name.", ""),
    ("TAPAS", FEST, AW, "", "", "", "Runs the TAPAS Music and Dance Festival.", ""),
    ("Kalakshetra Foundation", FEST, PUB, "Thiruvanmiyur", "Kalakshetra Foundation campus",
     "73rd Annual Art Festival · 18–27 Dec 2026", "Mostly dance-dramas; two Carnatic vocal concerts (20 and 27 Dec, 6 pm). Season tickets on MDnD.",
     "https://kalakshetra.in/others/programs-events/"),
    ("Live4You", FEST, ANN, "Egmore", "Museum Theatre, Pantheon Road", "Jyothirgamaya – Diya Dhvani Season 2 · 29 Dec 2026 – 3 Jan 2027",
     "Presents ticketed concerts listed on MDnD (29 & 30 Dec, 2 & 3 Jan, 6.30 pm); festival name and venue from indian-heritage.org.",
     "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("Show Space Event Solutions LLP", FEST, PUB, "Alwarpet / TTK Road", "The Music Academy, Madras",
     "Thamizhum Naanum (9th edition) · 6 Dec 2026",
     "Presents Sanjay Subrahmanyan's all-Tamil concert \"Thamizhum Naanum\" (6.30 pm; gates open 6 pm); tickets via the event website.",
     "https://www.thamizhumnaanum.com/"),
    ("Amazon Music", FEST, PUB, "", "Not stated", "Margazhi Experience · 19 Nov 2026",
     "Presents a free 6.30 pm \"Margazhi Experience\" concert by Sudha Ragunathan (MDnD listing); venue not printed.",
     "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("Anujan Broadcast & Sreedaya Trust", OTHER, AW, "Mylapore", "Ramanujar Millennium Hall", "", "", ""),
    ("Pranavakaram Fine Arts Trust", FEST, PUB, "Mylapore", "Bharatiya Vidya Bhavan Chennai Kendra", "Fundraiser concert · 16 Nov 2026",
     "Presents a ticketed fundraiser concert by Chitravina N. Ravikiran with Aditya Mohan (Hawaiian guitar), 6 pm at Bharatiya Vidya Bhavan Chennai Kendra (ragarasa.in listing).",
     "https://ragarasa.in/events/100th-annual-concerts-2026"),
    ("Beachville Coffee Roasters", FEST, PUB, "Alwarpet / TTK Road", "Beachville Coffee Roasters, 99 St. Mary's Road, Alwarpet", "A Carnatic Shot (2nd edition) · 21–26 Dec 2026",
     "Six short themed Carnatic sets in the café, 2.30 pm daily, ticketed (artists and times on MDnD). The 2025 edition was curated by Aalaap.",
     "https://www.indian-heritage.org/musicseason/sch.html"),
]

PART = "Some dates via artists' websites"
ORGS += [
    ("Mudhra", OTHER, PART, "T. Nagar", "Sri Thyaga Brahma Gana Sabha (Vani Mahal)", "", "Date found on Shashank's website.", ""),
    ("Sanjay Subrahmanyan", FEST, PART, "", "Muthamizh Peravai; Asian College of Journalism", "", "Presents his own Sanjay Sabha Live concert series.", "https://sanjaysub.com/"),
]
# organisers whose individual dates appear on artists' websites, before their own schedule is out
for i, row in enumerate(ORGS):
    if row[0] in {"Brahma Gana Sabha", "Sruthi Laya Kendra",
                  "Bharatiya Vidya Bhavan, Chennai Kendra", "Sri Thyaga Brahma Gana Sabha",
                  "The Indian Fine Arts Society", "Hamsadhwani", "Tamil Isai Sangam",
                  "Nada Sudha", "VVS Foundation & SaMaa Arts",
                  "Madhuradhwani", "Carnatica", "TTVV Trust & Cleveland Thyagaraja Festival", "Lakshman Sruthi",
                  "SciArtsRUs", "Sri Rama Bhaktha Jana Samaj", "Gayatri Fine Arts Global", "Asthika Samajam",
                  "Anujan Broadcast & Sreedaya Trust"}:
        ORGS[i] = row[:2] + (PART,) + row[3:6] + ("Own schedule not yet published; dates found on artists' websites.",) + row[7:]
out = [dict(name=n, group=g, status=s, area=a, venue=v, festival_2026=f, note=note, url=u)
       for n, g, s, a, v, f, note, u in ORGS]
assert len({o["name"] for o in out}) == len(out), "duplicate organisation"
Path(__file__).parent.joinpath("data/organisations.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(out), "organisations:", {s: sum(o["status"] == s for o in out) for s in (PUB, ANN, AW)})
