# Text to number mapping
frequency_text_to_number = {
    "Never": 0,
    "Rarely": 1,
    "Frequently": 2,
    "Almost always": 3,
    "Always": 4,
    "Not observed": None
}

# Number to text mapping
number_to_frequency_text = {}

for text, number in frequency_text_to_number.items():
    if number is not None:
        number_to_frequency_text[number] = text

#Calculates projected improvement in frequency after N semesters
#Business rule: +2 points per semester, with a maximum of 4.
def calculate_projection(current_frequency, semesters=1):
    value = frequency_text_to_number.get(current_frequency)

    if value is None:
        return "Not observed"

    new_value = value + 2 * semesters
    if new_value > 4:
        new_value = 4

    return number_to_frequency_text.get(new_value, "Not observed")
