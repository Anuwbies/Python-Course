raw_name = "  Mika Santos  "
course_label = "Python basics"

# Each method returns a new string. Keep the source values available.
clean_name = raw_name.strip()
upper_name = clean_name.upper()
updated_label = course_label.replace("basics", "foundations")

print(clean_name)
print(upper_name)
print(len(clean_name))
print(updated_label)
