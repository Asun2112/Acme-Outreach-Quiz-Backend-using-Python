#backend for potential Acme user intial quiz by Aditya Sunkam
QUESTIONS = {
    1: ("How would you describe your natural skin tone?", {
        'a': 'Very fair, pale white',
        'b': 'Fair, ivory or beige',
        'c': 'Light brown or olive',
        'd': 'Medium brown',
        'e': 'Dark brown',
        'f': 'Deeply pigmented, very dark'
    }),
    2: ("How does your skin react after sun exposure with no protection?", {
        'a': 'Always burns, never tans',
        'b': 'Burns easily, tans a bit',
        'c': 'Sometimes burns, tans slowly',
        'd': 'Rarely burns, tans well',
        'e': 'Almost never burns, tans deeply',
        'f': 'Never burns'
    }),
    # --- Skin-moisture questions (3-10) ---
    3: ("How visible are your facial pores (nose/forehead)?", {
        'a': 'Very visible',
        'b': 'Slightly visible',
        'c': 'Hardly visible'
    }),
    4: ("How often do you experience acne or blackheads?", {
        'a': 'Rarely',
        'b': 'Occasionally',
        'c': 'Frequently'
    }),
    5: ("Does your skin look shiny or feel oily by midday?", {
        'a': 'Never',
        'b': 'Sometimes',
        'c': 'Often'
    }),
    6: ("During cold, dry winters your skin feels…", {
        'a': 'Tight, flaky, rough',
        'b': 'Slightly dry',
        'c': 'Still normal or oily'
    }),
    7: ("In hot, humid weather your skin becomes…", {
        'a': 'Drier or irritated',
        'b': 'No big change',
        'c': 'Oilier / sticky'
    }),
    8: ("How often do you NEED moisturizer to feel comfortable?", {
        'a': 'Daily',
        'b': 'Sometimes',
        'c': 'Rarely / never'
    }),
    9: ("Which best describes your overall skin texture?", {
        'a': 'Dry or flaky',
        'b': 'Smooth',
        'c': 'Greasy / slippery'
    }),
    10: ("When trying new products, your skin is…", {
        'a': 'Very sensitive (burns/stings)',
        'b': 'Mildly reactive',
        'c': 'Rarely reacts'
    }),
    # --- Lifestyle / environment (11-15) ---
    11: ("Average sleep per night?", {
        'a': '<5 h', 'b': '6-7 h', 'c': '8 h+'
    }),
    12: ("Daily environment:", {
        'a': 'Mostly outdoors', 'b': 'Mix indoor/outdoor', 'c': 'Mostly indoors'
    }),
    13: ("Usual climate:", {
        'a': 'Hot & humid', 'b': 'Cold & dry', 'c': 'Mild / temperate'
    }),
    14: ("Seasonal skin change?", {
        'a': 'Drastic', 'b': 'Slight', 'c': 'None'
    }),
    15: ("Sun-protection habit?", {
        'a': 'Rarely', 'b': 'Sometimes', 'c': 'Always'
    })
}

# 2.  SCORING MAPS
FITZ_MAP      = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
MOISTURE_MAP  = {'a': -1, 'b': 0, 'c': 1}              # default
CLIMATE_MAP   = {'a':  1, 'b': -1, 'c': 0}             # Q13 special

# 3.  PRODUCT RECOMMENDATIONS  (by Fitzpatrick I-VI  ×  Dry/Normal/Oily)
RECOMMEND = {
    ("I", "Dry"):    "CeraVe Moisturizing Cream + Broad-Spectrum SPF 50",
    ("II", "Dry"):   "CeraVe Moisturizing Cream + SPF 50",
    ("III", "Dry"):  "La Roche-Posay Lipikar AP+M Balm",
    ("IV", "Dry"):   "Vanicream Lotion + Tinted Mineral SPF",
    ("V", "Dry"):    "Vaseline Cocoa Radiant Lotion",
    ("VI", "Dry"):   "Vaseline Cocoa Radiant + EltaMD UV Clear Deep Tint SPF 46",
    ("I", "Normal"): "Cetaphil Cleanser + Neutrogena Hydro Boost Gel",
    ("II", "Normal"): "Cetaphil + Hydro Boost + Zinc-Oxide SPF 50",
    ("III", "Normal"): "Hydro Boost Gel AM / light occlusive PM",
    ("IV", "Normal"): "Hydro Boost + EltaMD UV Clear Tinted SPF 46",
    ("V", "Normal"):  "Hydro Boost + EltaMD Deep Tint SPF 46",
    ("VI", "Normal"): "EltaMD Deep Tint + Night Antioxidant Serum",
    ("I", "Oily"):   "La Roche-Posay Effaclar Mat + Sal-Acid Cleanser",
    ("II", "Oily"):  "Effaclar Mat AM + Hydro Boost PM",
    ("III", "Oily"): "Effaclar Mat + Mineral SPF 30 + Adapalene 0.3 % PM",
    ("IV", "Oily"):  "Effaclar Mat + Tinted Moisturizer SPF",
    ("V", "Oily"):   "Effaclar Mat + Deep Tint SPF 46",
    ("VI", "Oily"):  "Effaclar Mat + EltaMD Deep Tint + Azelaic Serum"
}

# 4.validated answer
def prompt(qnum: int, text: str, opts: dict) -> str:
    print(f"\nQ{qnum}. {text}")
    for k, v in opts.items():
        print(f"   {k}) {v}")
    while True:
        choice = input("   Your choice → ").strip().lower()
        if choice in opts:
            return choice
        print("   ❌ Please enter one of:", "/".join(opts))


# 5.  MAIN QUIZ LOOP(going thru the keys)
def run_quiz():
    scores = {"fitz": 0, "moist": 0, "life": 0}

    for qnum, (qtext, optdict) in QUESTIONS.items():
        ans = prompt(qnum, qtext, optdict)

        # --- scoring logic ---
        if qnum in (1, 2):                       # Fitzpatrick
            scores["fitz"] += FITZ_MAP[ans]

        elif 3 <= qnum <= 10:                    # Moisture
            scores["moist"] += MOISTURE_MAP[ans]

        elif qnum == 13:                         # Climate
            scores["life"]  += CLIMATE_MAP[ans]

        else:                                    # Other lifestyle q's
            scores["life"]  += MOISTURE_MAP[ans]

    # interpret results
    fitz_avg  = round(scores["fitz"] / 2) or 1
    fitz_type = ["I","II","III","IV","V","VI"][fitz_avg-1]

    if   scores["moist"] > 2:  moist_type = "Oily"
    elif scores["moist"] < -2: moist_type = "Dry"
    else:                      moist_type = "Normal"

    life_tag = ("Skin-friendly lifestyle" if scores["life"] > 2 else
                "Skin-stressing lifestyle" if scores["life"] < -2 else
                "Neutral lifestyle impact")

    # recommendation lookup
    product = RECOMMEND.get((fitz_type, moist_type),
                            "No specific product match (use gentle basics)")

    # final print summary
    print("\n" + "="*45)
    print("  YOUR SKIN PROFILE")
    print(f"• Fitzpatrick Type:        {fitz_type}")
    print(f"• Skin Moisture Profile:   {moist_type}")
    print(f"• Lifestyle Impact:        {life_tag}")
    print("• Suggested product:", product)
    print("="*45)

# 6.  Run if executed directly
if __name__ == "__main__":
    run_quiz()