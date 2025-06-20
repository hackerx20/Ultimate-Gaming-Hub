
#options for the questions present in Questions.py (list of lists)
options = [
    ["Delhi", "Mumbai", "Kolkata", "Chennai"],  # Q1
    ["Rabindranath Tagore", "Bankim Chandra", "Sarojini Naidu", "Mahatma Gandhi"],  # Q2
    ["Earth", "Jupiter", "Mars", "Venus"],  # Q3
    ["Amazon", "Nile", "Yangtze", "Mississippi"],  # Q4
    ["B. R. Ambedkar", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel"],  # Q5
    ["Goa", "Sikkim", "Tripura", "Nagaland"],  # Q6
    ["Lion", "Elephant", "Tiger", "Peacock"],  # Q7
    ["Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Rajendra Prasad"],  # Q8
    ["Gold", "Iron", "Diamond", "Platinum"],  # Q9
    ["1947", "1950", "1930", "1942"],  # Q10
    ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],  # Q11
    ["Alexander Fleming", "Marie Curie", "Isaac Newton", "Louis Pasteur"],  # Q12
    ["J.K. Rowling", "Stephen King", "George Orwell", "Agatha Christie"],  # Q13
    ["Nitrogen", "Oxygen", "Carbon Dioxide", "Helium"],  # Q14
    ["Sydney", "Canberra", "Melbourne", "Perth"],  # Q15
    ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "James Watt"],  # Q16
    ["Mars", "Jupiter", "Venus", "Mercury"],  # Q17
    ["100°C", "0°C", "50°C", "200°C"],  # Q18
    ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"],  # Q19
    ["Sahara", "Gobi", "Kalahari", "Atacama"],  # Q20
    ["Peacock", "Eagle", "Sparrow", "Parrot"],  # Q21
    ["7", "5", "6", "8"],  # Q22
    ["Au", "Ag", "Hg", "Pb"],  # Q23
    ["Russia", "Canada", "USA", "China"],  # Q24
    ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"],  # Q25
    ["Heart", "Brain", "Liver", "Kidney"],  # Q26
    ["Camel", "Horse", "Elephant", "Donkey"],  # Q27
    ["1914", "1939", "1918", "1945"],  # Q28
    ["Paris", "Rome", "Berlin", "Madrid"],  # Q29
    ["Benjamin Franklin", "Thomas Edison", "Nikola Tesla", "Michael Faraday"],  # Q30
    ["Arctic", "Indian", "Atlantic", "Pacific"],  # Q31
    ["Mount Everest", "K2", "Mount Kilimanjaro", "Mount Elbrus"],  # Q32
    ["Neil Armstrong", "Yuri Gagarin", "Buzz Aldrin", "John Glenn"],  # Q33
    ["0°C", "50°C", "100°C", "20°C"],  # Q34
    ["France", "UK", "Italy", "Germany"],  # Q35
    ["Diamond", "Gold", "Platinum", "Iron"],  # Q36
    ["Lotus", "Rose", "Sunflower", "Marigold"],  # Q37
    ["Indira Gandhi", "Sonia Gandhi", "Sarojini Naidu", "Pratibha Patil"],  # Q38
    ["World Wide Web", "World Web Way", "Wide World Web", "Web Wide World"],  # Q39
    ["Greenland", "Australia", "Madagascar", "Borneo"],  # Q40
    ["Bankim Chandra Chattopadhyay", "Rabindranath Tagore", "Sarojini Naidu", "Mahatma Gandhi"],  # Q41
    ["H2O", "CO2", "O2", "N2"],  # Q42
    ["Mercury", "Venus", "Mars", "Earth"],  # Q43
    ["Greece", "China", "USA", "UK"],  # Q44
    ["Seismology", "Meteorology", "Oceanography", "Astronomy"],  # Q45
    ["O+", "O-", "AB+", "A+"],  # Q46
    ["Lion", "Elephant", "Tiger", "Leopard"],  # Q47
    ["Thomas Edison", "Nikola Tesla", "Benjamin Franklin", "Michael Faraday"],  # Q48
    ["Blue Whale", "Elephant", "Shark", "Giraffe"],  # Q49
    ["Saturn", "Jupiter", "Uranus", "Neptune"],  # Q50
    ["Avocado", "Tomato", "Cucumber", "Carrot"],  # Q51
    ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"],  # Q52
    ["Marie Curie", "Mother Teresa", "Rosalind Franklin", "Jane Austen"],  # Q53
    ["Japan", "China", "South Korea", "India"],  # Q54
    ["206", "208", "210", "212"],  # Q55
    ["Femur", "Humerus", "Radius", "Tibia"],  # Q56
    ["Rabindranath Tagore", "C.V. Raman", "Amartya Sen", "Mother Teresa"],  # Q57
    ["8", "7", "9", "10"],  # Q58
    ["France", "Germany", "Italy", "Spain"],  # Q59
    ["The Sun", "Moon", "Stars", "Clouds"],  # Q60
    ["Nile", "Amazon", "Yangtze", "Mississippi"],  # Q61
    ["Jupiter", "Saturn", "Mars", "Venus"],  # Q62
    ["Sardar Patel", "Jawaharlal Nehru", "Mahatma Gandhi", "Subhas Chandra Bose"],  # Q63
    ["Yen", "Won", "Yuan", "Dollar"],  # Q64
    ["Wright Brothers", "Thomas Edison", "Nikola Tesla", "James Watt"],  # Q65
    ["O", "O2", "CO2", "H2"],  # Q66
    ["Antarctica", "Siberia", "Greenland", "Iceland"],  # Q67
    ["6", "12", "8", "16"],  # Q68
    ["Venus", "Mars", "Mercury", "Jupiter"],  # Q69
    ["Mercury", "Lead", "Gold", "Silver"],  # Q70
    ["George Washington", "Abraham Lincoln", "John Adams", "Thomas Jefferson"],  # Q71
    ["Rome", "Milan", "Venice", "Naples"],  # Q72
    ["Kidney", "Liver", "Heart", "Lung"],  # Q73
    ["Ice Hockey", "Football", "Basketball", "Cricket"],  # Q74
    ["Albert Einstein", "Isaac Newton", "Stephen Hawking", "Galileo Galilei"],  # Q75
    ["Wilhelm Röntgen", "Marie Curie", "Isaac Newton", "Albert Einstein"],  # Q76
    ["Cell", "Tissue", "Organ", "Organism"],  # Q77
    ["Liver", "Heart", "Lung", "Kidney"],  # Q78
    ["James Watt", "Thomas Newcomen", "George Stephenson", "Nikola Tesla"],  # Q79
    ["Mango", "Apple", "Banana", "Orange"],  # Q80
    ["Helium", "Oxygen", "Hydrogen", "Carbon Dioxide"],  # Q81
    ["Burj Khalifa", "Eiffel Tower", "Statue of Liberty", "CN Tower"],  # Q82
    ["Cheetah", "Lion", "Tiger", "Leopard"],  # Q83
    ["Elephant", "Rhinoceros", "Hippopotamus", "Giraffe"],  # Q84
    ["China", "India", "USA", "Russia"],  # Q85
    ["Valentina Tereshkova", "Sally Ride", "Kalpana Chawla", "Mae Jemison"],  # Q86
    ["Jonas Salk", "Louis Pasteur", "Edward Jenner", "Marie Curie"],  # Q87
    ["Great Wall of China", "Berlin Wall", "Hadrian's Wall", "Western Wall"],  # Q88
    ["Pacific", "Atlantic", "Indian", "Arctic"],  # Q89
    ["Great Barrier Reef", "Red Sea Coral Reef", "New Caledonian Reef", "Mesoamerican Reef"],  # Q90
    ["Karnam Malleswari", "P. V. Sindhu", "Mary Kom", "Saina Nehwal"],  # Q91
    ["Moscow", "St. Petersburg", "Novosibirsk", "Sochi"],  # Q92
    ["Hummingbird", "Sparrow", "Crow", "Finch"],  # Q93
    ["New York", "Los Angeles", "Chicago", "Miami"],  # Q94
    ["Junko Tabei", "Bachendri Pal", "Anita Devi", "Santosh Yadav"],  # Q95
    ["Deoxyribonucleic Acid", "Deoxyribose Nucleic Acid", "Deoxyribonuclear Acid", "Dioxyribonucleic Acid"],  # Q96
    ["Tim Berners-Lee", "Bill Gates", "Steve Jobs", "Vint Cerf"],  # Q97
    ["Jupiter", "Saturn", "Mars", "Earth"],  # Q98
    ["Trans-Siberian Railway", "Canadian Pacific Railway", "Orient Express", "Indian Pacific Railway"],  # Q99
    ["English", "Mandarin", "Spanish", "Hindi"]  # Q100
]
