import json, math

# The markdown list as a string
markdown_list = """
1. Novice Adventurer
2. Rookie Explorer
3. Beginner Trailblazer
4. Junior Pathfinder
5. Emerging Wanderer
6. Greenhorn Voyager
7. Neophyte Discoverer
8. Apprentice Wayfarer
9. Tenderfoot Nomad
10. Initiate Seeker
11. Rookie Scout
12. Novitiate Pioneer
13. Trainee Wayfinder
14. Aspiring Nomad
15. Young Journeyer
16. Apprentice Voyager
17. Fresh Explorer
18. Junior Trailseeker
19. Promising Pathfinder
20. Novice Expeditionist
21. Intermediate Adventurer
22. Journeyman Explorer
23. Skilled Trailblazer
24. Adept Pathfinder
25. Expert Wanderer
26. Veteran Voyager
27. Seasoned Discoverer
28. Accomplished Wayfarer
29. Master Nomad
30. Proven Seeker
31. Elite Scout
32. Grandmaster Pioneer
33. Maestro Wayfinder
34. Virtuoso Nomad
35. Supreme Journeyer
36. Apex Explorer
37. Legendary Trailblazer
38. Mythic Pathfinder
39. Divine Wanderer
40. Transcendent Voyager
41. Celestial Discoverer
42. Eminent Wayfarer
43. Ascendant Nomad
44. Sovereign Seeker
45. Paramount Scout
46. Imposing Pioneer
47. Noble Wayfinder
48. Majestic Nomad
49. Royal Journeyer
50. Regal Explorer
51. Grand Adventurer
52. Illustrious Trailblazer
53. Prestigious Pathfinder
54. Distinguished Wanderer
55. Renowned Voyager
56. Exalted Discoverer
57. Supreme Wayfarer
58. Infinite Nomad
59. Eternal Seeker
60. Timeless Scout
61. Dimensional Pioneer
62. Cosmic Wayfinder
63. Ethereal Adventurer
64. Astral Trailblazer
65. Divine Pathfinder
66. Celestial Wanderer
67. Transcendent Voyager
68. Mythical Discoverer
69. Legendary Wayfarer
70. Immortal Nomad
71. Divine Seeker
72. Celestial Scout
73. Eternal Pioneer
74. Timeless Wayfinder
75. Infinite Nomad
76. Astral Journeyer
77. Cosmic Explorer
78. Ethereal Trailblazer
79. Ascended Pathfinder
80. Divine Wanderer
81. Celestial Voyager
82. Transcendent Discoverer
83. Mythic Wayfarer
84. Eternal Nomad
85. Legendary Seeker
86. Immortal Scout
87. Celestial Pioneer
88. Divine Wayfinder
89. Eternal Wanderer
90. Ascended Voyager
91. Mythic Discoverer
92. Celestial Trailblazer
93. Transcendent Pathfinder
94. Infinite Wayfarer
95. Immortal Nomad
96. Ethereal Seeker
97. Ascended Scout
98. Celestial Pioneer
99. Mythic Wayfinder
100. Divine Explorer
"""

# Split the string into lines
lines = markdown_list.split("\n")

# Remove empty lines
lines = [line for line in lines if line]

# Initialize the boundary for the first level
boundary = 100

# Create a dictionary where the keys are the numbers and the values are the levels
levels = {}
for line in lines:
    level_number = int(line.split(". ")[0])
    level_name = line.split(". ")[1]
    levels[level_number] = {"name": level_name, "boundary": boundary}
    # Increase the boundary by a factor of 1.2 for the next level
    boundary = int(boundary * 1.070)

# Convert the dictionary to a JSON string
json_string = json.dumps(levels, indent=4)

print(json_string)