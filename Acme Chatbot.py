#backend for potential Acme user intial quiz by Aditya Sunkam
questions = {
    1: ("What is your natural skin color without sun exposure?", {
        'a': 'Very fair, pale white',
        'b': 'Fair, ivory or beige',
        'c': 'Light brown or olive',
        'd': 'Medium brown',
        'e': 'Dark brown',
        'f': 'Deeply pigmented, very dark'
    }),
    2: ("How does your skin react to sun exposure (without sunscreen)?", {
        'a': 'Always burns, never tans',
        'b': 'Often burns, tans a little',
        'c': 'Sometimes burns, tans gradually',
        'd': 'Rarely burns, tans easily',
        'e': 'Almost never burns, tans deeply',
        'f': 'Never burns'
    }),
    3: ("Do you have visible pores, especially on your nose and forehead (T-zone)?", {
        'a': 'Yes, a lot',
        'b': 'A few',
        'c': 'Rarely or none'
    }),
    4: ("How often do you get pimples, blackheads, or acne?", {
        'a': 'Rarely',
        'b': 'Occasionally',
        'c': 'Frequently'
    }),
    5: ("Does your skin feel greasy or shiny by midday?", {
        'a': 'Never',
        'b': 'Sometimes',
        'c': 'Often'
    }),
    6: ("How does your skin feel in winter?", {
        'a': 'Very dry and uncomfortable',
        'b': 'Slightly dry',
        'c': 'Normal or still oily'
    }),
    7: ("How does your skin feel in hot/humid weather?", {
        'a': 'Uncomfortable dryness',
        'b': 'Normal',
        'c': 'Very oily, sticky'
    }),
    8: ("How often do you use moisturizer?", {
        'a': 'Daily, or my skin feels very dry',
        'b': 'Occasionally',
        'c': 'Rarely, I feel I don’t need it'
    }),
    9: ("How would you describe your skin texture?", {
        'a': 'Rough or flaky',
        'b': 'Smooth',
        'c': 'Slippery or oily'
    }),
    10: ("How sensitive is your skin to new products (burning, stinging, redness)?", {
        'a': 'Very sensitive',
        'b': 'Mild sensitivity',
        'c': 'Rarely sensitive'
    }),
    11: ("How would you rate your average sleep per night?", {
        'a': 'Less than 5 hours',
        'b': '6–7 hours',
        'c': '8 hours or more'
    }),
    12: ("Where do you spend most of your day?", {
        'a': 'Mostly outdoors',
        'b': 'A mix of indoor and outdoor',
        'c': 'Mostly indoors'
    }),
    13: ("What type of climate do you live in most of the year?", {
        'a': 'Hot and humid',
        'b': 'Cold and dry',
        'c': 'Moderate / mild'
    }),
    14: ("Does your skin change noticeably with the seasons?", {
        'a': 'Yes, drastically',
        'b': 'Slightly',
        'c': 'No, it stays the same'
    }),
    15: ("How often do you use sun protection (sunscreen, hats)?", {
        'a': 'Rarely',
        'b': 'Sometimes',
        'c': 'Always'
    })
}

# Scoring maps
fitz_map      = {'a': 1,  'b': 2,  'c': 3,  'd': 4,  'e': 5,  'f': 6}
moisture_map  = {'a': -1, 'b': 0,  'c': 1}
climate_map   = {'a': 1,  'b': -1, 'c': 0}          # Q13 only

#Avoding errors for invalid responses
def get_answer(qnum: int, opts: dict[str, str]) -> str:
    while True:
        reply = input("   Your choice: ").strip().lower()
        if reply in opts:
            return reply
        print("  Invalid choice. Please enter one of:", "/".join(opts))

# Main quiz loop
scores = {"fitz": 0, "moisture": 0, "lifestyle": 0}

print("Skin-Type & Lifestyle Quiz\n" + "-" * 40)
for qnum, (qtext, options) in questions.items():
    print(f"\nQ{qnum}. {qtext}")
    for key, desc in options.items():
        print(f"   {key}) {desc}")
    ans = get_answer(qnum, options)

    # update scores
    if qnum in (1, 2):
        scores["fitz"] += fitz_map[ans]
    elif 3 <= qnum <= 10:
        scores["moisture"] += moisture_map[ans]
    elif qnum == 13:          # climate question
        scores["lifestyle"] += climate_map[ans]
    else:
        scores["lifestyle"] += moisture_map[ans]

# Interpreting results
fitz_type = f"Fitzpatrick Type {round(scores['fitz'] / 2)}"
if scores["moisture"] > 2:
    moisture_type = "Oily"
elif scores["moisture"] < -2:
    moisture_type = "Dry"
else:
    moisture_type = "Normal"

if scores["lifestyle"] > 2:
    lifestyle_tag = "Skin-friendly lifestyle"
elif scores["lifestyle"] < -2:
    lifestyle_tag = "Skin-stressing lifestyle"
else:
    lifestyle_tag = "Neutral lifestyle impact"

#Display final results
print("\n" + "-" * 40 + "\n🧾  Final Assessment")
print(f"• {fitz_type}")
print(f"• Skin-moisture profile: {moisture_type}")
print(f"• Lifestyle impact:      {lifestyle_tag}")
print("-" * 40)