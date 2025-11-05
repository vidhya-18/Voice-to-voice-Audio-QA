"""
Simple script to generate test audio files for the Voice Q&A application
"""
from gtts import gTTS
import os

# Test audio content
test_scripts = {
    "test_1_simple.mp3": """
    Hello, this is a test audio file. My name is Alex and I work as a software engineer.
    I enjoy coding in Python and building AI applications. Today is a sunny day and I'm 
    excited to test this voice Q&A system.
    """,
    
    "test_2_story.mp3": """
    Once upon a time, there was a small village nestled in the mountains. The village 
    was called Riverside because a beautiful river flowed through it. In this village 
    lived a young girl named Emma who loved to read books. Every day after school, 
    Emma would go to the library and read stories about adventures and magic. Her 
    favorite book was about a dragon who learned to be kind.
    """,
    
    "test_3_facts.mp3": """
    Here are some interesting facts about space. The sun is 93 million miles away 
    from Earth. It takes light from the sun about 8 minutes to reach us. Jupiter 
    is the largest planet in our solar system, and it has a giant storm called 
    the Great Red Spot that has been raging for over 400 years. Saturn has beautiful 
    rings made of ice and rock particles.
    """,
    
    "test_4_recipe.mp3": """
    Today I will share my favorite chocolate chip cookie recipe. First, preheat 
    your oven to 350 degrees Fahrenheit. In a large bowl, cream together one cup 
    of softened butter with three-quarters cup of white sugar and three-quarters 
    cup of brown sugar. Add two eggs and two teaspoons of vanilla extract. In 
    another bowl, mix two and a quarter cups of flour, one teaspoon of baking soda, 
    and one teaspoon of salt. Gradually blend the dry ingredients into the wet 
    mixture. Finally, stir in two cups of chocolate chips. Bake for 9 to 11 minutes.
    """,
    
    "test_5_meeting.mp3": """
    Good morning everyone, welcome to today's team meeting. First on our agenda 
    is the quarterly sales report. Our sales team has exceeded targets by 15 percent 
    this quarter, which is excellent news. Second, we need to discuss the upcoming 
    product launch scheduled for next month. The marketing team has prepared several 
    campaign ideas that we'll review. Finally, we'll talk about the new office 
    policies that will take effect from next week. Let's start with the sales report.
    """
}

def generate_test_audios():
    """Generate multiple test audio files"""
    
    # Create a test_audio directory
    output_dir = "test_audio"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎵 Generating test audio files...\n")
    
    for filename, text in test_scripts.items():
        try:
            print(f"Creating: {filename}")
            
            # Generate speech
            tts = gTTS(text=text.strip(), lang='en', slow=False)
            
            # Save to file
            filepath = os.path.join(output_dir, filename)
            tts.save(filepath)
            
            print(f"✅ Saved: {filepath}\n")
            
        except Exception as e:
            print(f"❌ Error creating {filename}: {str(e)}\n")
    
    print(f"🎉 Done! All test audio files are in the '{output_dir}' folder")
    print("\n📋 Test Audio Files Created:")
    print("  1. test_1_simple.mp3 - Simple introduction")
    print("  2. test_2_story.mp3 - Short story about a girl")
    print("  3. test_3_facts.mp3 - Space facts")
    print("  4. test_4_recipe.mp3 - Cookie recipe")
    print("  5. test_5_meeting.mp3 - Team meeting transcript")
    print("\n💡 Sample Questions You Can Ask:")
    print("  For test_1: 'What is the person's name?' or 'What does Alex do?'")
    print("  For test_2: 'What was the girl's name?' or 'What was her favorite book about?'")
    print("  For test_3: 'How far is the sun from Earth?' or 'Which planet has rings?'")
    print("  For test_4: 'What temperature should I preheat the oven?' or 'How many eggs do I need?'")
    print("  For test_5: 'What is the first agenda item?' or 'How much did sales exceed targets?'")

if __name__ == "__main__":
    # Check if gtts is installed
    try:
        from gtts import gTTS
        generate_test_audios()
    except ImportError:
        print("❌ Error: gTTS not installed")
        print("Run: uv pip install gtts")
        print("Then run this script again")