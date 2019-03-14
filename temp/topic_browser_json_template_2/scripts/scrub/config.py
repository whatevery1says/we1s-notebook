# -*- coding: utf-8 -*-
##########################################
# Configuration file for scrub.py        #
# Must be in the same folder as scrub.py #
# See README file for instructions       #
##########################################

# File Configurations
input_file_path = "../../caches/text_files/"
output_file_path = "../../caches/text_files_clean/"
stopwords_location = ""
save_log = False

# Options
options = [
    # Iterations 1 -- Initial Processing
    {
    "Comment": "Standardizes all occurrences of \"United States of America\" to \"United States\".",
    "values": [
        {
        "find": "United States of America",
        "replace":"United States"
        }
        ]
    },
    # Iteration 2 -- Punctuation
    {
    "values": [
        # Double slashes required in replace for raw strings
        {"find": "\.(\w)", "replace": ". \\1"},
        {"find": "\.(\w)", "replace": ": \\1"},
        {"find": "\.(\w)", "replace": "? \\1"}        
        ]
    },
    # Iteration 3 -- Tokenisation
    {
    "values": [
        {
        "find": "Affordable Care Act",
        "replace": "Affordable_Care_Act"
        },
        {
        "find": "American Association of University Professors",
        "replace": "AAUP"
        },
        {
        "find": "American Studies Association",
        "replace": "American_Studies_Association"
        },
        {
        "find": "Art History",
        "replace": "Art_History"
        },
        {
        "find": "center-left",
        "replace": "center_left"
        },
        {
        "find": "centre-left",
        "replace": "center_left"
        },
        {
        "find": "Chronicle of Higher Education",
        "replace": "Chronicle_of_Higher_Education"
        },
        {
        "find": "Cold War",
        "replace": "Cold_War"
        },
        {
        "find": "Common Core",
        "replace": "Common_Core"
        },
        {"find": "Department of Education",
        "replace": "Department_of_Education"
        },
        {
        "find": "distance learning",
        "replace": "distance_learning"
        },
        {
        "find": "East Coast",
        "replace": "East_Coast"
        },
        {
        "find": "East Asian",
        "replace": "East_Asian"
        },
        {
        "find": "hard headed",
        "replace": "hard_headed"
        },
        {
        "find": "hard nosed",
        "replace": "hard_nosed"
        },
        {
        "find": "hard science",
        "replace": "hard_science"
        },
        {
        "find": "hard sciences",
        "replace": "hard_sciences"
        },
        {
        "find": "hard times",
        "replace": "hard_times"
        },
        {
        "find": "hard wired",
        "replace": "hard_wired"
        },
        {
        "find": "hard work",
        "replace": "hard_work"
        },
        {
        "find": "hard working",
        "replace": "hard_working"
        },
        {
        "find": "Harvard University",
        "replace": "Harvard_University"
        },
        {
        "find": "H\\. M\\. O\\.",
        "replace": "HMO"
        },
        {
        "find": "American left",
        "replace": "American_left"
        },
        {
        "find": "British left",
        "replace": "British_left"
        },
        {
        "find": "left leaning",
        "replace": "left_leaning"
        },
        {
        "find": "left wing",
        "replace": "left_wing"
        },
        {
        "find": "the left",
        "replace": "the_left"
        },
        {
        "find": "American right",
        "replace": "American_right"
        },
        {
        "find": "British right",
        "replace": "British_right"
        },
        {
        "find": "right brain",
        "replace": "right_brain"
        },
        {
        "find": "right leaning",
        "replace": "right_leaning"
        },
        {
        "find": "right wing",
        "replace": "right_wing"
        },
        {
        "find": "the right",
        "replace": "the_right"
        },
        {
        "find": "Letters to the Editor",
        "replace": "Letters_to_the_Editor"
        },
        {
        "find": "liberal art(\\.)",
        "replace": "liberal_arts"
        },
        {
        "find": "liberal arts",
        "replace": "liberal_arts"
        },
        {
        "find": "liberal-arts",
        "replace": "liberal_arts"
        },
        {
        "find": "liberal-art(\\.)",
        "replace": "liberal_arts"
        },
        {
        "find": "Long Island",
        "replace": "Long_Island"
        },
        {
        "find": "long term",
        "replace": "long_term"
        },
        {
        "find": "long-term",
        "replace": "long_term"
        },
        {
        "find": "Los Angeles",
        "replace": "los_angeles"
        },
        {
        "find": "English major(\\.)",
        "replace": "english_major"
        },
        {
        "find": "English majors",
        "replace": "english_major"
        },
        {
        "find": "History major(\\.)",
        "replace": "history_major"
        },
        {
        "find": "History majors",
        "replace": "history_major"
        },
        {
        "find": "Philosophy major(\\.)",
        "replace": "philosophy_major"
        },
        {
        "find": "Philosophy majors",
        "replace": "philosophy_major"
        },
        {
        "find": "French major(\\.)",
        "replace": "french_major"
        },
        {
        "find": "French majors",
        "replace": "french_major"
        },
        {
        "find": "Classics major(\\.)",
        "replace": "classics_major"
        },
        {
        "find": "Classics major",
        "replace": "classics_major"
        },
        {
        "find": "Art major(\\.)",
        "replace": "art_major"
        },
        {
        "find": "Art majors",
        "replace": "art_major"
        },
        {
        "find": "Arts major(\\.)",
        "replace": "arts_major"
        },
        {
        "find": "Arts majors",
        "replace": "arts_major"
        },
        {
        "find": "Language major(\\.)",
        "replace": "language_major"
        },
        {
        "find": "Language majors",
        "replace": "language_major"
        },
        {
        "find": "humanities major(\\.)",
        "replace": "humanities_major"
        },
        {
        "find": "humanities majors",
        "replace": "humanities_major"
        },
        {
        "find": "Art History major(\\.)",
        "replace": "art_history_major"
        },
        {
        "find": "Art History majors",
        "replace": "art_history_major"
        },
        {
        "find": "major in the humanities",
        "replace": "major_in_the_humanities"
        },
        {
        "find": "English minor(\\.)",
        "replace": "english_minor"
        },
        {
        "find": "English minors",
        "replace": "english_minor"
        },
        {
        "find": "History minor(\\.)",
        "replace": "history_minor"
        },
        {
        "find": "History minors",
        "replace": "history_minor"
        },
        {
        "find": "Philosophy minor(\\.)",
        "replace": "philosophy_minor"
        },
        {
        "find": "Philosophy minors",
        "replace": "philosophy_minor"
        },
        {
        "find": "French minor(\\.)",
        "replace": "french_minor"
        },
        {
        "find": "French minors",
        "replace": "french_minor"
        },
        {
        "find": "Classics minor(\\.)",
        "replace": "classics_minor"
        },
        {
        "find": "Classics minors",
        "replace": "classics_minor"
        },
        {
        "find": "Art minor(\\.)",
        "replace": "art_minor"
        },
        {
        "find": "Art minors",
        "replace": "art_minor"
        },
        {
        "find": "Arts minor(\\.)",
        "replace": "arts_minor"
        },
        {
        "find": "Arts minors",
        "replace": "arts_minor"
        },
        {
        "find": "Language minor(\\.)",
        "replace": "language_minor"
        },
        {
        "find": "Language minors",
        "replace": "language_minor"
        },
        {
        "find": "humanities minor(\\.)",
        "replace": "humanities_minor"
        },
        {
        "find": "humanities minors",
        "replace": "humanities_minors"
        },
        {
        "find": "Art History minor(\\.)",
        "replace": "art_history_minor"
        },
        {
        "find": "Art History minors",
        "replace": "art_history_minor"
        },
        {
        "find": "minor in the humanities",
        "replace": "minor_in_the_humanities"
        },
        {
        "find": "M\\. D\\. s",
        "replace": "M_D"
        },
        {
        "find": "M\\. D\\.",
        "replace": "M_D"
        },
        {
        "find": "Middle East",
        "replace": "Middle_East"
        },
        {
        "find": "Middle Eastern",
        "replace": "Middle_East"
        },
        {
        "find": "M\\. A\\.",
        "replace": "M_A"
        },
        {
        "find": "MacArthur Foundation",
        "replace": "MacArthur_Foundation"
        },
        {
        "find": "Modern Language Association",
        "replace": "MLA"
        },
        {
        "find": "National Endowment for the Humanities",
        "replace": "NEH"
        },
        {
        "find": "N\\. E\\. H\\.",
        "replace": "NEH"
        },
        {
        "find": "National Endowment for the Arts",
        "replace": "NEA"
        },
        {
        "find": "N\\. E\\. A\\.",
        "replace": "NEA"
        },
        {
        "find": "National Endowment for the Humanities",
        "replace": "National_Endowment_for_the_Humanities"
        },
        {
        "find": "National Humanities Center",
        "replace": "National_Humanities_Center"
        },
        {
        "find": "National Commission on Excellence in Education",
        "replace": "National_Commission_on_Excellence_in_Education"
        },
        {
        "find": "New Left",
        "replace": "new_left"
        },
        {
        "find": "New Jersey",
        "replace": "New_Jersey"
        },
        {
        "find": "New York",
        "replace": "New_York"
        },
        {
        "find": "North America",
        "replace": "North_America"
        },
        {
        "find": "North American",
        "replace": "North_American"
        },
        {
        "find": "part time",
        "replace": "part_time"
        },
        {
        "find": "Ph.D.",
        "replace": "PhD"
        },
        {
        "find": "queer studies",
        "replace": "queer_studies"
        },
        {
        "find": "queer theory",
        "replace": "queer_theory"
        },
        {
        "find": "Rockefeller Foundation",
        "replace": "Rockefeller_Foundation"
        },
        {
        "find": "social science(\\.)",
        "replace": "social_science\\1"
        },
        {
        "find": "social sciences",
        "replace": "social_sciences"
        },
        {
        "find": "social scientist",
        "replace": "social_scientist"
        },
        {
        "find": "social studies",
        "replace": "social_studies"
        },
        {
        "find": "South America",
        "replace": "South_America"
        },
        {
        "find": "South American",
        "replace": "South_America"
        },
        {
        "find": "The National Review",
        "replace": "The_National_Review"
        },
        {
        "find": "University of California",
        "replace": "University_of_California"
        },
        {
        "find": "University of Chicago",
        "replace": "University_of_Chicago"
        },
        {
        "find": "University of Bridgeport",
        "replace": "University_of_Bridgeport"
        },
        {
        "find": "U\\. S\\.",
        "replace": "U_S"
        },
        {
        "find": "United States",
        "replace": "U_S"
        },
        {
        "find": "Wall Street Journal",
        "replace": "Wall_Street_Journal"
        },
        {
        "find": "Yale University",
        "replace": "Yale_University"
        },
        {
        "find": "centre",
        "replace": "center"
        },
        {
        "find": "labour",
        "replace": "labor"
        },
        {
        "find": "organisations",
        "replace": "organizations"
        },
        {
        "find": "programme",
        "replace": "program"
        },
        {
        "find": "Associated Press",
        "replace": "[.]"
        },
        {
        "find": "Continue reading the main story",
        "replace": "[.]"
        },
        {
        "find": "Corrections & Amplifications",
        "replace": "[.]"
        },
        {
        "find": "Credit: By",
        "replace": "[.]"
        },
        {
        "find": "New York Times",
        "replace": "[.]"
        },
        {
        "find": "njtowns@nytimes.com",
        "replace": "[.]"
        },
        {
        "find": "N.Y. / Region",
        "replace": "[.]"
        },
        {
        "find": "Published:",
        "replace": "[.]"
        },
        {
        "find": "Room for Debate",
        "replace": "[.]"
        },
        {
        "find": "Special to the New York Times",
        "replace": "[.]"
        },
        {
        "find": "Sunday New Jersy Section",
        "replace": "[.]"
        },
        {
        "find": "620 Eighth Avenue, New York, N.Y. 10018-1405",
        "replace": "[.]"
        },
        {
        "find": "'s",
        "replace": "[.]"
        },
        {
        "find": "ʼs",
        "replace": "[.]"
        }
        ]
    },
    # Iteration 4 -- Extra Processing
    {
    "values": []
    }
]