#test file to ensure the proper functionality of the compiler 
# Walking steps calculation
total_students = 90
total_steps = 0
distance_km = 0.5  # Assuming the distance between CIT Lab and the stadium is 0.5 km
steps_per_km = 1312  # Average number of steps per km for a fast-paced walk

# Calculate total steps for all students
total_steps = total_students * (distance_km * steps_per_km)

# Calculate average steps per student
average_steps = total_steps / total_students
print(f"Average number of steps required per student: {average_steps}")
