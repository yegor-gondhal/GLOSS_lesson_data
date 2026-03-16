import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://gloss.dliflc.edu/") # Get website
wait = WebDriverWait(driver, 5, poll_frequency=0.01)

# Get the language selections
languages_container = driver.find_element(By.ID, "LanguageSelectorDivContainer")
languages = languages_container.find_elements(By.CSS_SELECTOR, "label")

# Get the level selections
level_container = driver.find_element(By.ID, "LevelSelectorDDL")
levels = level_container.find_elements(By.CSS_SELECTOR, "option")

# Get the modality selections
modality_container = driver.find_element(By.ID, "ModalitySelectorDDL")
modalities = modality_container.find_elements(By.CSS_SELECTOR, "option")

# Get the competence selections
competence_container = driver.find_element(By.ID, "CompetenceSelectorDDL")
competences = competence_container.find_elements(By.CSS_SELECTOR, "option")

# Get the topic selections
topic_container = driver.find_element(By.ID, "TopicSelectorDDL")
topics = topic_container.find_elements(By.CSS_SELECTOR, "option")

# Get the video selector checkbox
video_selector = driver.find_element(By.ID, "VideoSelectorInput")

# Get the search button
search_button = driver.find_element(By.ID, "lessonSearchBtn")

# Initiate DataFrame
df = pd.DataFrame({
    "Language": [],
    "Level": [],
    "Modality": [],
    "Competence": [],
    "Topic": [],
    "Video": [],
    "Lessons": []
})

# Create function to extract number of lessons
def get_number(x):
    if not (x[7].isdigit()):
        return None

    idx = 7
    while x[idx].isdigit():
        idx += 1
    return int(x[7:idx])



for language in languages: # Iterate through each Language
    language.click()
    for level in levels: # Iterate through each Level
        level.click()
        for modality in modalities: # Iterate through each Modality
            modality.click()
            for competence in competences: # Iterate through each Competence
                competence.click()
                for topic in topics: # Iterate through each topic
                    topic.click()
                    if video_selector.is_selected(): # Unselect video_selector if selected
                        video_selector.click()
                    # wait for changes to apply
                    wait.until(lambda d: d.find_element(By.ID, "lessonSearchBtn").is_enabled())
                    # Extract number of lessons
                    lessons = get_number(search_button.text)
                    # Create new row
                    data = [language.text, level.text, modality.text, competence.text, topic.text, False, lessons]
                    # Add to the DataFrame
                    df.loc[len(df)] = data
                    # Check the video_selector option
                    video_selector.click()
                    # Wait for changes to apply
                    wait.until(lambda d: d.find_element(By.ID, "lessonSearchBtn").is_enabled())
                    # Extract number of lessons
                    lessons = get_number(search_button.text)
                    # Change previous row
                    data[5] = True
                    data[6] = lessons
                    # Add to DataFrame
                    df.loc[len(df)] = data

# Turn DataFrame to a csv
df.to_csv("data.csv", index=False)