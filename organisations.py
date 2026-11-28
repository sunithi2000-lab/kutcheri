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
    # 2026-11-26: the society's own schedule PDF (1 Dec – 3 Jan) on season.mylaporetimes.com
    ("Kartik Fine Arts", MAJOR, PUB, "Alwarpet / TTK Road", "Narada Gana Sabha, TTK Road; Bharatiya Vidya Bhavan, Mylapore", "52nd Year Art Festival 2026 · 1 Dec 2026 – 3 Jan 2027",
     "From the society's own schedule PDF (season.mylaporetimes.com, read 26 Nov 2026). 1–12 Dec at Narada Gana Sabha Main Hall: inauguration 1 Dec 6 pm, then Amritha Murali 7 pm; two concerts a day (4 or 4.30 pm and 6.45 pm), ticketed (season and daily tickets on MDnD). 13 Dec – 3 Jan at Bharatiya Vidya Bhavan Main and Mini Halls: up to six concerts a day (10 am to 7 pm), incl. the 29th Tamil Isai Vizha (26 Dec – 1 Jan) and an NRI Music Festival (2–3 Jan); entry not printed. Dance (incl. a dance festival at Narada Gana Sabha Mini Hall to 27 Jan), harikatha, seminars and school group items are not listed here.",
     "https://season.mylaporetimes.com/schedules-2026/Kartik-Fine-Arts.pdf"),
    ("Narada Gana Sabha", MAJOR, PUB, "Alwarpet / TTK Road", "TTK Road, Teynampet", "Isai Natya Nataka Vizha 2026 · 13 Dec 2026 – 1 Jan 2027",
     "Ticketed concerts at 3.30 pm and 6.30 pm (6 pm on some days), 13–31 Dec, on the sabha's MDnD page; dance, discourse and bhajan items (19, 22 and 31 Dec, 1 Jan) are not listed here. Season passes on MDnD (Members and All Season Pass 13 Dec – 1 Jan; Core Season Pass 20 Dec – 1 Jan).",
     "https://mdnd.in/SeasonTickets/OrganizerLandingPage?ci=101&r_id=2400"),
    ("Sri Krishna Gana Sabha", MAJOR, PUB, "T. Nagar", "Dr. Nalli Gana Vihar, 20 Maharajapuram Santhanam Salai",
     "70th Margazhi Mela · 12 Dec 2026 – 3 Jan 2027", "Music and dance; tickets on tikkl.com. Natya Kala Conference (dance) 26–28 Dec.",
     "https://krishnaganasabha.com/assets/images/nkc/margazhimela2026/MM_schedule(2026).pdf"),
    # 2026-11-27: MDnD's Chennai Carnatic listing now names the sabha as organiser of its 6.30 pm concerts at Vani Mahal
    ("Sri Thyaga Brahma Gana Sabha", MAJOR, PUB, "T. Nagar", "Vani Mahal, G.N. Road", "December Music Festival 2026–27 · 10 Dec 2026 – 9 Jan 2027 (listed so far)", "Ticketed 6.30 pm concerts at Vani Mahal, 10 Dec – 9 Jan, listed on MDnD under the sabha's name (read 27 Nov 2026; also on NatyaNetwork at \"Swaminathan Vani Mahal\"); a few further concerts come from artists' sites (S. J. Jananiy 19 Dec 4 pm). vanimahal.com shows no 2026–27 programme yet; untitled 6.30 pm items on 5, 6, 13 and 15 Jan (NatyaNetwork) are not listed here.", "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    # 2026-11-29: the sabha's December festival (10–31 Dec) on MDnD's Chennai Carnatic listing
    ("Brahma Gana Sabha", MAJOR, PUB, "Mylapore", "Rasika Ranjani Sabha, Mylapore", "December festival 2026 · 10–31 Dec 2026 (listed so far)",
     "Ticketed concerts at 6.15 pm, 10–31 Dec, listed on MDnD under \"Brahma Gana Sabha\" (read 29 Nov 2026; no venue printed there – the artists' own pages place the sabha's concerts at Rasika Ranjani Sabha, Mylapore). Sanjay Subrahmanyan's 1 Jan 9.30 am concert comes from his site. Season.mylaporetimes.com lists the sabha (index entry 13) but its schedule PDF is not out yet.",
     "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("Mylapore Fine Arts Club", MAJOR, PUB, "Mylapore", "45 Musiri Subramaniam Road", "75th Year Art Festival · 17 Dec 2026 – 16 Jan 2027",
     "Music 18 Dec – 1 Jan: free morning concerts at 9 am and 10.15 am (\"All are welcome\"; 9.30 am on 1 Jan) and two ticketed concerts a day at 4 pm and 6.30 pm (season tickets Rs 5,900 reserved / Rs 1,770 unreserved from 7 Dec at the club office; daily and season tickets on MDnD), from the club's own schedule PDF (season.mylaporetimes.com, read 25 Nov 2026) and its MDnD page. 2–16 Jan is the dance festival (not listed here); a 22 Dec upanyasam and a 23 Dec classical-meets-film programme are not listed either.",
     "https://season.mylaporetimes.com/schedules-2026/Mylapore-Fine-Arts-Club.pdf"),
    ("Sri Parthasarathy Swami Sabha", MAJOR, PUB, "Mylapore", "Vidya Bharathi Kalyana Mandapam, Bheemasena Garden Road",
     "126th Year Isai Vizha · 17 Dec 2026 – 3 Jan 2027", "Two ticketed concerts daily, 4 pm and 6.30 pm, 17 Dec – 2 Jan, on the sabha's MDnD festival page (venue Vidya Bharathi Kalyana Mandapam); Shashank & Abhishek Raghuram 3 Jan, 6.30 pm, at Narada Gana Sabha (artist's site; now on MDnD). Dance and drama on 3, 4 and 6 Jan at Narada Gana Sabha are not listed here.",
     "https://mdnd.in/SeasonTickets/OrganizerLandingPage?ci=101&r_id=2304"),
    ("The Indian Fine Arts Society", MAJOR, PUB, "Alwarpet / TTK Road", "Ethiraja Kalyana Nilayam, TTK Road", "Annual Music Festival 2026–27 · 18–29 Dec 2026 (listed so far)", "Two ticketed concerts a day, 4.30 pm and 7 pm, 18–29 Dec, from NatyaNetwork's Margazhi 2026 listing (24 Nov 2026); the society's own festival page gives 17 Dec as the start and its brochure is an image not yet read. A namasankeerthanam (20 Dec) and an abhang programme (21 Dec) are not listed here.", "https://natyanetwork.com/margazhi?day=all&type=music"),
    ("Rasika Ranjani Sabha", MAJOR, AW, "Mylapore", "Dakshinamoorthy Auditorium", "", "", "https://rrsabha.org/"),
    ("Bharatiya Vidya Bhavan, Chennai Kendra", MAJOR, PUB, "Mylapore", "Pottipati Gnanamba Obul Reddy Auditorium, East Mada Street",
     "Bhavan's Margazhi Mahotsav 2026 (first edition) · 20 Nov – 12 Dec 2026",
     "With South Zone Cultural Centre. Free (all are welcome): 4.30 pm and 6.45 pm daily, some 10.30 am slots, from the Kendra's programme schedule PDF. Bhajans, discourses, harikatha, dance and film-based items are not listed here.",
     "https://www.bhavanschennai.org/assets/images/event/14112026_BHAVANS_Margazhi_Cultural_2026ProgrammeSchedule.pdf"),
    ("Tamil Isai Sangam", MAJOR, ANN, "George Town", "Rajah Annamalai Mandram, Esplanade Road", "Annual music festival · December 2026",
     "Ticketed 6.30 pm concerts on 22, 23 and 30 Dec listed on MDnD under \"Tamil Isai Sangam\" (read 29 Nov 2026; no venue printed – the Sangam's hall is Raja Annamalai Mandram). Full programme not yet seen.", ""),
    # 2026-11-28: Margazhi Maha Utsavam Series (1–11 Dec) on chennaievent.com's season listing
    ("Hamsadhwani", MAJOR, PUB, "Adyar", "Youth Hostel Auditorium, Indira Nagar", "Margazhi Maha Utsavam 2026 · 1–11 Dec 2026",
     "Two themed concerts a day, 4.45 pm and 6.45 pm, 1–11 Dec, at the Youth Hostel Auditorium, Indira Nagar, from chennaievent.com's season listing (read 28 Nov 2026; \"Seat 1st cum 1st\"; the listing names no organiser – Marghazhi Maha Utsavam is Hamsadhwani's festival per season.mylaporetimes.com). Free entry per the artists' own pages. A musical discourse (10 Dec), a musical lecture (11 Dec 4.45 pm) and a moderated Bharathi programme (11 Dec 6.45 pm) are not listed here.", "https://chennaievent.com/index_search.php?q=Kamarajar"),
    ("Asthika Samajam", MAJOR, AW, "Alwarpet", "Venus Colony", "", "", ""),
    ("Chromepet Cultural Academy", OTHER, AW, "Chromepet", "", "", "Margazhi Festival.", ""),
    ("Thrimoorthi Sangeetha Sabha", OTHER, AW, "", "", "", "", ""),
    ("Sri Krishna Fine Arts Society", OTHER, AW, "Nanganallur", "", "", "", ""),
    ("Meenakshi Sundararajan Fine Arts Academy", OTHER, AW, "", "", "", "", ""),
    ("Music Education Trust", OTHER, AW, "", "", "", "", ""),
    ("Shri Purandaradaasar Trust", OTHER, AW, "", "", "", "Music festival.", ""),
    ("Sampoornam Foundation for Music and Arts", FEST, AW, "Mylapore", "Arkay Convention Centre", "", "Margazhi Music Festival.", ""),
    ("Naadhabrahmam", FEST, AW, "Mylapore", "Srinivasa Sastri Hall, Luz", "", "Sangeetha Raga Mahothsavam.", ""),
    ("Trinity Arts", FEST, ANN, "Mylapore", "Rasika Ranjani Sabha", "Trinity Arts Festival 2026 · from Nov 2026", "Festival at R.R. Sabha; S. J. Jananiy's 21 Nov concert comes from the artist's website. Full programme not yet found.", ""),
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
    ("Sat Sangam Sabha", OTHER, ANN, "Madipakkam", "Sri Sath Sangam (Ramanujar Hall), Madipakkam", "37th Year Annual Music/Dance Festival · from 2 Jan 2027", "Festival opens 2 Jan 2027 (inauguration and award 5.30 pm, inaugural concert by Paramakudi S. Ravindran 6.45 pm); daily tickets Rs 100 at the hall from 15 Dec (chennaievent.com listing). Concerts 3–5 Jan (4 pm on 3 and 4 Jan; 6.45 pm daily) also on that listing; rest of the programme not yet seen.", "https://chennaievent.com/index_search.php?q=Kamarajar"),
    ("Chennai Cultural Academy Trust", OTHER, AW, "", "", "", "", ""),
    # 2026-11-29: found on chennaievent.com's season listing (Panchami and monthly concerts)
    ("Sri Thiagaraja Sangeetha Vidwath Samajam", OTHER, ANN, "Mylapore", "Thyagarajapuram, near Madhava Perumal Koil, Mylapore", "Panchami and monthly concerts · 8 and 18 Dec 2026",
     "Mylapore samajam (\"Regd\"). Saxophone Panchami concert by G. Ramanathan (8 Dec, 6.30 pm) and a mandolin monthly concert by Nidhi Hariharan (18 Dec, 6 pm), from chennaievent.com's season listing (read 29 Nov 2026; phones 98410 31680 / 98400 64292). Entry not printed.", "https://chennaievent.com/index_search.php?q=Kamarajar"),
    # 2026-11-26: pre-music festival programme (1–10 Dec), its own schedule PDF on season.mylaporetimes.com
    ("Naada Inbam", FEST, PUB, "Mylapore", "Ragasudha Hall, 85/2 Luz Avenue", "Pre-music festival · 1–10 Dec 2026; December Music Festival · 11 Dec 2026 – 10 Jan 2027",
     "December Music Festival (dedicated to the memory of Shri S.V. Krishnan): three free concerts most days (10 am, 4 pm, 6.15 pm), 11 Dec – 10 Jan, incl. mic-less nagaswaram mornings (12 and 14 Dec), the B. Doraiswamy centenary (23 Dec), \"Vandanamu\" for Prof. T. Viswanathan (2–3 Jan) and \"Guruvamsham\" for Palghat Raghu (9 Jan) – \"All Concerts are free for the public\", donations welcome (own schedule PDF, read 28 Nov 2026). Pre-music festival 1–10 Dec: concerts at 10 am, 3 pm, 4.15 pm and 6.15 pm (incl. \"A Weekend with Dikshitar\", 4–6 Dec), entry not printed. Harikatha, lectures, lecture-demonstrations, a dance item and prize functions are not listed here.",
     "https://season.mylaporetimes.com/schedules-2026/Naada-Inbam.pdf"),
    ("Charsur Arts Foundation", FEST, PUB, "Teynampet", "My Bungalow, 40 Eldams Road",
     "DVAYAM – Sounds of Duality · 15–31 Dec 2026", "Two concerts daily, 4 pm and 6.30 pm (plus some 10 am slots); programme for 15–30 Dec listed on MDnD; 31 Dec 6.30 pm A.S. Murali from NatyaNetwork's listing. Lecture-demonstrations not included.",
     "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("Chennai Fine Arts", FEST, AW, "", "", "", "", ""),
    ("Madhuradhwani", FEST, ANN, "Mylapore", "Arkay Convention Centre, Luz", "ACC 16th Anniversary Music Festival · 21 Nov – 6 Dec 2026; December Season 7 Dec 2026 – 13 Jan 2027",
     "Runs the Arkay Convention Center (ACC). 16-day anniversary festival opens 21 Nov with mangala isai (3.30 pm), inauguration (5.15 pm) and Neyveli R. Santhanagopalan (6.30 pm); a December Season of over 200 concerts follows, 7 Dec – 13 Jan (Mylapore Times, 18 Nov 2026). Full programme not yet published; K.S. Vishnudev's 23 Nov and 10 Dec concerts come from the artist's poster.",
     "https://www.mylaporetimes.com/2026/11/music-festival-over-16-days-to-mark-16th-anniversary-of-arkay-center-luz/"),
    ("Sunaadalahari", FEST, AW, "Abhiramapuram", "Indira Ranganathan Trust, 52 C.P. Ramaswamy Road", "", "Garden-setting concerts.", ""),
    ("Carnatica", FEST, PUB, "Thiruvanmiyur", "Sri Sankara Vidhyashramam School Auditorium, Thiruvanmiyur", "Global Heritage Music & Arts Fest 2026 · 11–22 Dec 2026",
     "Presented with Sri Parthasarathy Swami Sabha: two ticketed concerts a day (4.30 pm and 6.45 pm; 4 pm and 6.30 pm on 14 and 20 Dec), 11–22 Dec, listed on MDnD; venue from indian-heritage.org. Two non-Carnatic items (18 Dec piano–vocal with Madhan Karky, 21 Dec film music) and a 19 Dec katha kutcheri are not listed here; Kunnakudi M. Balamuralikrishna 19 Dec 6.45 pm from NatyaNetwork's listing. Also co-presented Bharat Sangeet Utsav 2026 (31 Oct – 7 Nov, before the season).",
     "https://mdnd.in/SeasonTickets/OrganizerLandingPage?ci=101&r_id=30992"),
    ("MDnD", FEST, PUB, "Mylapore", "MDnD Performance Centre, Luz Church Road", "Anandha Margazhi · 12–26 Dec 2026", "Anandha Margazhi: a free 10 am concert every day, 12–26 Dec 2026, listed on MDnD as \"... for Anandha Margazhi\" (read 29 Nov 2026; venue not printed). MDnD also sells season tickets for many sabhas.","https://www.mdnd.in/seasontickets"),
    # 2026-11-21: 28th Annual Music Festival programme (24 Dec – 13 Jan so far) found on chennaievent.com's season listing
    ("Nada Sudha", FEST, PUB, "Velachery", "Sri Ganapathi Sachchidananda Ashram Hall, Velachery", "28th Annual Music Festival · 24 Dec 2026 – 13 Jan 2027 (listed so far)",
     "Three concerts a day (2.30 pm, 4 pm, 6.15 pm) at the Ashram hall, from chennaievent.com's season listing (which names no organiser; artists' own pages name Nada Sudha for its concerts). Season donor pass by phone (98849 49597 / 91763 09996). A thematic film-based concert, a fusion-style item and two items of unclear format are not listed here.",
     "https://chennaievent.com/index_search.php?q=Kamarajar"),
    ("Sruthi Laya Kendra", FEST, ANN, "Mylapore", "Bharatiya Vidya Bhavan, Mylapore", "39th Winter Music Festival · 26 Dec 2026", "Winter Music Festival at the Bhavan main auditorium on 26 Dec: 9 am \"Layataranga\" percussion ensemble led by Giridhar Udupa, then award presentations and Shashank's flute recital (chennaievent.com, read 29 Nov 2026; Shashank's site: 11 am).", ""),
    ("Gayatri Fine Arts Global", FEST, AW, "Mylapore", "Sri Krishna Saras Hall, P.S. Sivaswamy Salai", "", "", ""),
    ("Shakthi Sangita Sabha", FEST, AW, "Valasaravakkam", "Anbu Nagar", "", "", ""),
    ("SASTRA Satsangh", FEST, AW, "Vadapalani", "SASTRA Chennai Campus, AVM Road, Vadapalani", "", "Margazhi Mela.", ""),
    ("TTVV Trust & Cleveland Thyagaraja Festival", FEST, AW, "Teynampet", "Tattvaloka Hall, Eldams Road", "", "Margazhi Mela.", ""),
    ("VVS Foundation & SaMaa Arts", FEST, AW, "Mylapore", "Raghavendra Swami Mutt, Salai Street; Sri Srikara Anjaneya Raghavendra Swamy Sannidhanam, near R.R. Sabha", "Ekaantha Sangeetha Seva (early-morning concerts)", "Swagatham and Ekaantha Sangeetha Seva festivals.", ""),
    ("Kauvery Margazhi Maha Utsavam", FEST, AW, "", "", "", "Organiser name not found; listed under the festival name.", ""),
    ("Lalitha Jewellery", FEST, AW, "Valasaravakkam", "Jyothi Indira Thirumana Mandapam", "", "Runs the Jyothi Indira Margazhi Yuvautsav.", ""),
    # 2026-11-20: Chennaiyil Thiruvaiyaru Season 16 dates (casualwalker.com 2026–27 festival guide, citing the festival's Instagram post)
    ("Lakshman Sruthi", FEST, AW, "Teynampet", "Kamarajar Arangam, Anna Salai", "Chennaiyil Thiruvaiyaru Season 16 · 21–27 Dec 2026", "Runs the Chennaiyil Thiruvaiyaru festival. Sid Sriram (22 Dec) and Sudha Ragunathan (23 Dec), 7.15 pm, found on chennaievent.com; full programme not yet seen.", ""),
    ("Chennaiyil Sangeeth Utsav", FEST, PUB, "Neelankarai", "R.K Convention Centre", "Chennaiyil Sangeeth Utsav Season 5 · 9–14 Jan 2027", "Four ticketed 6.30 pm concerts listed on MDnD (9, 10, 12, 13 Jan 2027); venue R.K Convention Centre, Neelankarai (indian-heritage.org). Organiser name not found; listed under the festival name.", "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("RASOHAM", FEST, ANN, "Alwarpet", "Rasoham, Alwarpet", "Kutty Kutchery Festival 2026 · 12–21 Dec 2026",
     "Ten-day festival at 28 Murray's Gate Road, Alwarpet. Programme published (indian-heritage.org, 24 Nov 2026): ten 6–7.15 pm \"performative conversations\" (Hindustani, folk, dance, saxophone, percussion), none a Carnatic concert, so none are listed here.",
     "https://www.indian-heritage.org/musicseason/2627/kuttykutchery.html"),
    ("Medai The Stage", FEST, AW, "Alwarpet", "1st Cross St, Co-operative Colony", "", "", ""),
    ("Triplicane Music Festival", FEST, AW, "Triplicane", "NKT Muthu Hall", "", "Organiser name not found; listed under the festival name.", ""),
    ("TAPAS", FEST, AW, "", "", "", "Runs the TAPAS Music and Dance Festival.", ""),
    ("Kalakshetra Foundation", FEST, PUB, "Thiruvanmiyur", "Kalakshetra Foundation campus",
     "73rd Annual Art Festival · 18–27 Dec 2026", "Mostly dance-dramas; two Carnatic vocal concerts (20 and 27 Dec, 6 pm). Season tickets on MDnD.",
     "https://kalakshetra.in/others/programs-events/"),
    ("Live4You", FEST, ANN, "Egmore", "Museum Theatre, Pantheon Road", "Jyothirgamaya – Diya Dhvani Season 2 · 29 Dec 2026 – 3 Jan 2027",
     "Presents ticketed concerts listed on MDnD (29 & 30 Dec, 2 & 3 Jan, 6.30 pm; 31 Dec, 2 & 3 Jan, 3.30 pm) and a free 3.30 pm nagaswaram–mandolin–veena trio on 29 Dec (NatyaNetwork); festival name and venue from indian-heritage.org. Hindustani concerts (30 & 31 Dec) are not listed here.",
     "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("Show Space Event Solutions LLP", FEST, PUB, "Alwarpet / TTK Road", "The Music Academy, Madras",
     "Thamizhum Naanum (9th edition) · 6 Dec 2026",
     "Presents Sanjay Subrahmanyan's all-Tamil concert \"Thamizhum Naanum\" (6.30 pm; gates open 6 pm); tickets via the event website.",
     "https://www.thamizhumnaanum.com/"),
    ("Amazon Music", FEST, PUB, "", "Not stated", "Margazhi Experience · 19 Nov 2026",
     "Presents a free 6.30 pm \"Margazhi Experience\" concert by Sudha Ragunathan (MDnD listing); venue not printed.",
     "https://mdnd.in/ViewEvents/Carnatic?ci=101&c=3659&eMode=All&Date=All&mc=8&mcName=Carnatic"),
    ("Anujan Broadcast & Sreedaya Trust", OTHER, PUB, "Mylapore", "Sri Ramanujar Millennium Hall", "December season concerts · 15–31 Dec 2026",
     "Also listed as \"Anujan Broadcasts and Sri Dayaa Trust\". Ticketed concerts at 4 pm and 6.30 pm, 15–31 Dec, from NatyaNetwork's Margazhi 2026 listing (tickets on MDnD). An abhang (devotional) programme on 20 Dec is not listed here.",
     "https://natyanetwork.com/margazhi"),
    ("Pranavakaram Fine Arts Trust", FEST, PUB, "Mylapore", "Bharatiya Vidya Bhavan Chennai Kendra", "Fundraiser concert · 16 Nov 2026",
     "Presents a ticketed fundraiser concert by Chitravina N. Ravikiran with Aditya Mohan (Hawaiian guitar), 6 pm at Bharatiya Vidya Bhavan Chennai Kendra (ragarasa.in listing).",
     "https://ragarasa.in/events/100th-annual-concerts-2026"),
    ("Eswara Ganothsavam", FEST, PUB, "Mylapore", "Durgabai Deshmukh Centenary Auditorium, Andhra Mahila Sabha", "Eswara Ganothsavam 2026 (4th year) · 27 Dec 2026",
     "Festival of the compositions of Dr. Thamarasseri Eswaran Bhattathiri; 27 Dec 6.30 pm concert by Neyveli R. Santhanagopalan (from the festival poster). The poster names no organiser, so it is listed under the festival name.",
     "https://sunithi2000-lab.github.io/kutcheri/sources/posters/eswara-ganothsavam-2026.jpg"),
    ("Beachville Coffee Roasters", FEST, PUB, "Alwarpet / TTK Road", "Beachville Coffee Roasters, 99 St. Mary's Road, Alwarpet", "A Carnatic Shot (2nd edition) · 21–26 Dec 2026",
     "Six short themed Carnatic sets in the café, 2.30 pm daily, ticketed (artists and times on MDnD). The 2025 edition was curated by Aalaap.",
     "https://www.indian-heritage.org/musicseason/sch.html"),
]

ORGS += [
    ("World Brahmins Welfare Association", OTHER, PUB, "", "Panigraha", "WBWA 13th anniversary celebrations · 3 Jan 2027",
     "Anniversary celebration with an award ceremony and a Carnatic vocal concert by S. J. Jananiy, 5 pm (artist's website).", "https://sjjananiy.com/shows"),
    ("Psiog", FEST, PUB, "Mylapore", "Srinivasa Sastri Hall, Luz Church Road", "Srothovaham Music Festival 2026 (3rd edition) · 5–13 Dec 2026",
     "Edition 3: \"Rooted. Rising. Resonance\". Two concerts a day (4.30 or 5 pm and 6.45 pm) at Srinivasa Sastri Hall, from chennaievent.com's season listing (read 27 Nov 2026; organiser not printed there – the festival is Psiog's per indian-heritage.org). A harikatha (5 Dec) and a moderated special presentation (12 Dec) are not listed here; entry not printed.", "https://www.indian-heritage.org/musicseason/2627/srothovaham.html"),
    ("Tamil Cultural Academy", OTHER, PUB, "R.A. Puram", "Image Auditorium, Raja Annamalaipuram", "31st year celebrations · 19–20 Dec 2026",
     "Spoorthi Rao's \"Tribute to the Female Trinity\" on 19 Dec (NatyaNetwork listing); its Mega Isai Vizha and film-hits shows are not listed here.", "https://natyanetwork.com/margazhi"),
    ("Minnaminni", FEST, PUB, "Alwarpet / TTK Road", "Medai – The Stage, Alwarpet", "Mélange Fest · 15 Nov 2026",
     "J.B. Sruthi Sagar flute concert on 15 Nov (NatyaNetwork listing); a storytelling item is not listed here.", "https://natyanetwork.com/margazhi"),
]

PART = "Some dates via artists' websites"
ORGS += [
    ("Mudhra", OTHER, ANN, "T. Nagar", "Vani Mahal (Obul Reddy Hall), G.N. Road", "32nd Fine Arts Festival · 1–27 Dec 2026",
     "Inauguration and awards on 1 Dec, 5.30 pm, at Obul Reddy Hall (Vani Mahal Mini Hall), followed by Shashank's flute concert (listed here). The 2–27 Dec programme (one concert a day at 6.15 pm) is published (livechennai.com, 9 Nov 2026) but is streamed online on Paalam TV and the Mudhrabhaskar YouTube channel with no hall printed, so those concerts are not listed here.",
     "https://www.livechennai.com/detailnews.asp?newsid=84566"),
    ("Sanjay Subrahmanyan", FEST, PART, "", "Muthamizh Peravai; Asian College of Journalism", "", "Presents his own Sanjay Sabha Live concert series.", "https://sanjaysub.com/"),
]
# organisers whose individual dates appear on artists' websites, before their own schedule is out
for i, row in enumerate(ORGS):
    if row[0] in {
                  "VVS Foundation & SaMaa Arts",
                  "TTVV Trust & Cleveland Thyagaraja Festival", "Lakshman Sruthi",
                  "SciArtsRUs", "SASTRA Satsangh", "Sri Rama Bhaktha Jana Samaj", "Gayatri Fine Arts Global", "Asthika Samajam",
                  }:
        ORGS[i] = row[:2] + (PART,) + row[3:6] + ("Own schedule not yet published; dates found on artists' websites.",) + row[7:]
# 2026-11-19: the website lists December and January only; these organisers' 2026–27 concerts were all in November
NOV_ONLY = {"Amazon Music", "Pranavakaram Fine Arts Trust", "Minnaminni", "Trinity Arts"}
for i, row in enumerate(ORGS):
    if row[0] in NOV_ONLY:
        ORGS[i] = row[:6] + ("November concert(s) only, so none are listed here (this list covers December and January). " + row[6],) + row[7:]
    elif row[0] in {"Bharatiya Vidya Bhavan, Chennai Kendra", "Madhuradhwani"}:
        ORGS[i] = row[:6] + (row[6] + " November concerts are not listed (this list covers December and January).",) + row[7:]
out = [dict(name=n, group=g, status=s, area=a, venue=v, festival_2026=f, note=note, url=u)
       for n, g, s, a, v, f, note, u in ORGS]
assert len({o["name"] for o in out}) == len(out), "duplicate organisation"
Path(__file__).parent.joinpath("data/organisations.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(out), "organisations:", {s: sum(o["status"] == s for o in out) for s in (PUB, ANN, AW)})
