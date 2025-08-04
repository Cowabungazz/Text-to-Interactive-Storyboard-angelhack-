from fastapi import APIRouter, HTTPException, Path, Body
from typing import List
from src.model.Lesson import Lesson
from src.model.LessonInDB import LessonInDB
from src.db.Lessons import (
    create_lesson,
    get_lesson,
    get_lessons,
    update_lesson,
    delete_lesson
)
from src.controllers.LinktoJson import fetch_json_from_url, convert_text_to_json
from src.controllers.GPTService import generate_lesson_from_text
from src.db.Lessons import lessons_collection

from src.db.Lessons import get_lessons
from src.model.LessonInDB import LessonInDB

router = APIRouter()
def validate_lesson_data(lesson_data: dict) -> bool:
    required_scene_keys = {"scene_id", "text", "icons", "branching"}
    required_branching_keys = {"decision_point", "next_scenes"}

    for scene in lesson_data.get("scenes", []):
        if not required_scene_keys.issubset(scene):
            print("here1/n")
            return False
        if not required_branching_keys.issubset(scene.get("branching", {})):
            print("here2/n")
            return False
    return "language" in lesson_data 

from bson import ObjectId

def lesson_helper(lesson) -> LessonInDB:
    lesson["_id"] = str(lesson["_id"])
    return LessonInDB(**lesson)

async def create_lesson(lesson: Lesson) -> LessonInDB:
    lesson_dict = lesson.dict()
    result = await lessons_collection.insert_one(lesson_dict)
    new_lesson = await lessons_collection.find_one({"_id": result.inserted_id})
    return lesson_helper(new_lesson)


@router.post("/submit-lesson-text/", response_model=LessonInDB)
async def submit_lesson_text_endpoint(text: str = Body(...), language: str = Body(...)):
    # prompt = f"""
    # I want you to create a scenario-based lesson on financial literacy for the elderly. The lesson should be engaging and educational, utilizing scenes where characters interact through dialogue or narrative text. Each scene should include text and a set of icons representing the characters or objects involved in the scene. The icons should be positioned using specific x and y coordinates, assuming height is 100 and width is 100. The lesson should also include branching choices where applicable, allowing the story to progress based on user decisions.

    # Here is the JSON format to follow for each scene in the lesson:
    # {{
    #   "lesson_id": 1,
    #   "scenes": [
    #     {{
    #       "scene_id": 1,
    #       "text": "This will be any form of text, a non-exhaustive example is a two-way conversation to illustrate the conversation the character icons are having.",
    #       "icons": [
    #         {{
    #           "icon_id": "icon1",
    #           "position": {{
    #             "x": 90.0,
    #             "y": 10.0
    #           }}
    #         }},
    #         {{
    #           "icon_id": "icon2",
    #           "position": {{
    #             "x": 10.0,
    #             "y": 90.0
    #           }}
    #         }}
    #       ],
    #       "branching": {{
    #         "decision_point": "choice1",
    #         "next_scenes": {{
    #           "option1": 2,
    #           "option2": 3
    #         }}
    #       }}
    #     }},
    #     {{
    #       "scene_id": 2,
    #       "text": "This will be any form of text, a non-exhaustive example is a two-way conversation to illustrate the conversation the character icons are having.",
    #       "icons": [
    #         {{
    #           "icon_id": "icon3",
    #           "position": {{
    #             "x": 50.0,
    #             "y": 50.0
    #           }}
    #         }}
    #       ],
    #       "branching": {{
    #         "decision_point": "choice2",
    #         "next_scenes": {{
    #           "option1": 4,
    #           "option2": 5
    #         }}
    #       }}
    #     }}
    #     // Add more scenes as needed (do not include this //..statement..)
    #   ],
    #   "language": "{language}"
    # }}

    # Edge cases:
    # - If there is only one option to branch to (aka no decision making to be made), include only that option in "next_scenes".
    # - If its the end of the storyboard, include "branching": {{"decision_point": "exit", "next_scenes": {{}}}}.

    # Ensure the JSON is valid and complete. Use the following icons in the scenes:

    # **Savings**
    # - icon11: piggy_bank, https://cdn-icons-png.flaticon.com/512/5488/5488049.png
    # - icon12: dollar_sign, https://static.vecteezy.com/system/resources/previews/009/341/093/original/money-icon-dollar-sign-design-free-png.png
    # - icon13: Bag with dollar sign, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLgu3mH2ZdXvYKqSMFGrGVIaf9th-It1yswpQm3ZV5gA&s
    # - icon14: Bank, https://cdn-icons-png.flaticon.com/512/2830/2830284.png
    # - icon15: CPF, https://www.cpf.gov.sg/content/dam/web/member/who-we-are/images/CPF%20Logo_FA-01%20(2).png
    # - icon16: Money burning, inflation, https://cdn-icons-png.flaticon.com/512/5068/5068223.png
    # - icon17: Budget, https://cdn-icons-png.flaticon.com/512/781/781831.png
    # - icon18: Debt, https://cdn-icons-png.flaticon.com/512/3535/3535361.png

    # **Insurance**
    # - icon21: hand with shield, https://cdn-icons-png.flaticon.com/512/5455/5455507.png
    # - icon22: health insurance, https://icons.veryicon.com/png/o/object/warning-icon/health-insurance-1.png
    # - icon23: protection from risk, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHzNp_5n2JNhoiZ3BwKrKJFBptXAXJA0K2cw&s
    # - icon24: critical illness insurance, https://cdn2.iconfinder.com/data/icons/life-insurance-innovicons-color/128/button-Critical_illness-insurance-hospital-shield-512.png
    # - icon25: insurance for property, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLUkKgeetGQrB6CdEMfaMqi31jBf6l2iuC1A&s
    # - icon26: personal accident insurance, https://cdn-icons-png.flaticon.com/512/2300/2300379.png
    # - icon27: Life insurance, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRI21Nb8VbCFTTuukjlmvNQ8Kwg-3eCybX6TA&s

    # **Investment**
    # - icon31: hand with positive growth chart, https://cdn-icons-png.flaticon.com/512/4221/4221633.png
    # - icon32: Hand with plant-nurturing and growth of investments, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxXtMjfQmv2ZPuIV-ODzcJqWw8r025HCNDtg&s
    # - icon33: bonds, https://cdn-icons-png.flaticon.com/512/3776/3776157.png
    # - icon34: stock profit, https://cdn-icons-png.flaticon.com/256/6513/6513831.png
    # - icon35: Investment Portfolio, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE0PbLkYsSRlHlYxLRQB10xl_aqMnWHwP5HQ&s
    # - icon36: Coins Stack, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQATHNwAtdIoA22s7v_EJebfNGsnRByl2CnA2o41v4fDw&s
    # - icon37: Buy button, https://cdn-icons-png.flaticon.com/512/600/600231.png
    # - icon38: Sell button, https://cdn-icons-png.flaticon.com/512/4106/4106603.png
    # - icon39: Calculator, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2REBWhSfmpWv9bGJTPTaJRjIN_901GhUN7Q&s
    # - icon391: Low/medium/high risk, https://img.freepik.com/premium-vector/risk-meter-icon-set-scale-low-medium-high-risk-speedometer_349999-1938.jpg

    # **Town**
    # - icon41: Town, https://cdn.storyboardthat.com/storyboard-creator/thumbs/5201_Large.webp
    # - icon42: Town-sun shining, https://cdn.storyboardthat.com/storyboard-creator/thumbs/12306_Large.webp
    # - icon43: City in background, https://cdn.storyboardthat.com/storyboard-creator/thumbs/8492_Large.webp

    # Here is the article or research to base the lesson on:
    # {text}

    # Please ensure the lesson is tailored for elderly learners and emphasizes key concepts of financial literacy.
    # """

    prompt = f"""
    I want you to create a detailed and structured scenario-based lesson on financial literacy for the elderly. The lesson should be engaging and educational, utilizing scenes where characters interact through dialogue or narrative text. Each scene must include text and a set of icons representing the characters or objects involved in the scene. The icons should be positioned using specific x and y coordinates, assuming height is 100 and width is 100. Each scene must also include branching choices where applicable, allowing the story to progress based on user decisions.

    Follow this exact JSON format for each scene in the lesson:
    {{
      "lesson_id": 1,
      "scenes": [
        {{
          "scene_id": 0,
          "text": "A detailed text describing the scene. Example: 'Mr. Tan discusses with his advisor about retirement plans.'",
          "icons": [
            {{
              "icon_id": "icon1.png",
              "position": {{
                "x": 90.0,
                "y": 10.0
              }}
            }},
            {{
              "icon_id": "icon2.png",
              "position": {{
                "x": 10.0,
                "y": 90.0
              }}
            }}
          ],
          "branching": {{
            "decision_point": "choice1 description", 
            "next_scenes": {{
              "describeOption1InCamelCase": 2, //the key must be underscored
              "describeOption2InCamelCase": 3 //the key must be underscored
            }}
          }}
        }},
        {{
          "scene_id": 1,
          "text": "A detailed text for scene 2.",
          "icons": [
            {{
              "icon_id": "icon3.png",
              "position": {{
                "x": 50.0,
                "y": 50.0
              }}
            }}
          ],
          "branching": {{
            "decision_point": "choice2 description",
            "next_scenes": {{
              "describeOption1InCamelCase": 4, //the key must be underscored
              "describeOption2InCamelCase": 5 //the key must be underscored
            }}
          }}
        }}
        // Add more scenes as needed
      ],
      "language": "{language}"
    }}

    Every scene must have "branching", these are the Edge cases:
    - If there is no branch needed and there is a next scene then go next scene, do this "branching": {{
            "decision_point": "",
            "next_scenes": {{
              "Next_scene": -2 
            }}
          }}
    - If there are no more next scenes to go to, "branching": {{"decision_point": "", "next_scenes": {{"Finish" = -1}}}}.

    Ensure the JSON is valid and complete. Use the following icons in the scenes:

    **Savings**
    - icon11: piggy_bank, https://cdn-icons-png.flaticon.com/512/5488/5488049.png
    - icon12: dollar_sign, https://static.vecteezy.com/system/resources/previews/009/341/093/original/money-icon-dollar-sign-design-free-png.png
    - icon13: Bag with dollar sign, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLgu3mH2ZdXvYKqSMFGrGVIaf9th-It1yswpQm3ZV5gA&s
    - icon14: Bank, https://cdn-icons-png.flaticon.com/512/2830/2830284.png
    - icon15: CPF, https://www.cpf.gov.sg/content/dam/web/member/who-we-are/images/CPF%20Logo_FA-01%20(2).png
    - icon16: Money burning, inflation, https://cdn-icons-png.flaticon.com/512/5068/5068223.png
    - icon17: Budget, https://cdn-icons-png.flaticon.com/512/781/781831.png
    - icon18: Debt, https://cdn-icons-png.flaticon.com/512/3535/3535361.png

    **Insurance**
    - icon21: hand with shield, https://cdn-icons-png.flaticon.com/512/5455/5455507.png
    - icon22: health insurance, https://icons.veryicon.com/png/o/object/warning-icon/health-insurance-1.png
    - icon23: protection from risk, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHzNp_5n2JNhoiZ3BwKrKJFBptXAXJA0K2cw&s
    - icon24: critical illness insurance, https://cdn2.iconfinder.com/data/icons/life-insurance-innovicons-color/128/button-Critical_illness-insurance-hospital-shield-512.png
    - icon25: insurance for property, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLUkKgeetGQrB6CdEMfaMqi31jBf6l2iuC1A&s
    - icon26: personal accident insurance, https://cdn-icons-png.flaticon.com/512/2300/2300379.png
    - icon27: Life insurance, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRI21Nb8VbCFTTuukjlmvNQ8Kwg-3eCybX6TA&s

    **Investment**
    - icon31: hand with positive growth chart, https://cdn-icons-png.flaticon.com/512/4221/4221633.png
    - icon32: Hand with plant-nurturing and growth of investments, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxXtMjfQmv2ZPuIV-ODzcJqWw8r025HCNDtg&s
    - icon33: bonds, https://cdn-icons-png.flaticon.com/512/3776/3776157.png
    - icon34: stock profit, https://cdn-icons-png.flaticon.com/256/6513/6513831.png
    - icon35: Investment Portfolio, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE0PbLkYsSRlHlYxLRQB10xl_aqMnWHwP5HQ&s
    - icon36: Coins Stack, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQATHNwAtdIoA22s7v_EJebfNGsnRByl2CnA2o41v4fDw&s
    - icon37: Buy button, https://cdn-icons-png.flaticon.com/512/600/600231.png
    - icon38: Sell button, https://cdn-icons-png.flaticon.com/512/4106/4106603.png
    - icon39: Calculator, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2REBWhSfmpWv9bGJTPTaJRjIN_901GhUN7Q&s
    - icon391: Low/medium/high risk, https://img.freepik.com/premium-vector/risk-meter-icon-set-scale-low-medium-high-risk-speedometer_349999-1938.jpg

    **Town**
    - icon41: Town, https://cdn.storyboardthat.com/storyboard-creator/thumbs/5201_Large.webp
    - icon42: Town-sun shining, https://cdn.storyboardthat.com/storyboard-creator/thumbs/12306_Large.webp
    - icon43: City in background, https://cdn.storyboardthat.com/storyboard-creator/thumbs/8492_Large.webp

    **Humans**
    - icon51: man in green shirt and blue jeans, https://cdn2.iconfinder.com/data/icons/city-basic-people/160/kid02-512.png
    - icon52: man in blue overalls, https://cdn0.iconfinder.com/data/icons/isometric-farm-people/240/farmer-01-512.png

    **Arrow**
    - icon61: next, https://cdn.pixabay.com/photo/2013/07/13/10/33/arrow-157494_1280.png

    Here is the article or research to base the lesson on:
    {text}

    Please ensure the lesson is tailored for elderly learners and emphasizes key concepts of financial literacy.
    """
    lesson_json = await generate_lesson_from_text(prompt)
    lesson_data = lesson_json  # since lesson_json is already a dict
    print(lesson_data)
    
    if not validate_lesson_data(lesson_data):
        raise HTTPException(status_code=400, detail="Invalid lesson data structure")

    lesson = Lesson(**lesson_data)
    new_lesson = await create_lesson(lesson)
    return new_lesson




@router.post("/submit-lesson-link/", response_model=LessonInDB)
async def submit_lesson_link_endpoint(url: str = Body(...), language: str = Body(...)):
    json_data = await fetch_json_from_url(url)
    prompt = f"""
    I want you to create a detailed and structured scenario-based lesson on financial literacy for the elderly. The lesson should be engaging and educational, utilizing scenes where characters interact through dialogue or narrative text. Each scene must include text and a set of icons representing the characters or objects involved in the scene. The icons should be positioned using specific x and y coordinates, assuming height is 100 and width is 100. Each scene must also include branching choices where applicable, allowing the story to progress based on user decisions.

    Follow this exact JSON format for each scene in the lesson:
    {{
      "lesson_id": "A detailed title describing the lesson",
      "scenes": [
        {{
          "scene_id": 1,
          "text": "A detailed text describing the scene. Example: 'Mr. Tan discusses with his advisor about retirement plans.'",
          "icons": [
            {{
              "icon_id": "icon1",
              "position": {{
                "x": 90.0,
                "y": 10.0
              }}
            }},
            {{
              "icon_id": "icon2",
              "position": {{
                "x": 10.0,
                "y": 90.0
              }}
            }}
          ],
          "branching": {{
            "decision_point": "choice1",
            "next_scenes": {{
              "option1": 2,
              "option2": 3
            }}
          }}
        }},
        {{
          "scene_id": 2,
          "text": "A detailed text for scene 2.",
          "icons": [
            {{
              "icon_id": "icon3",
              "position": {{
                "x": 50.0,
                "y": 50.0
              }}
            }}
          ],
          "branching": {{
            "decision_point": "choice2",
            "next_scenes": {{
              "option1": 4,
              "option2": 5
            }}
          }}
        }}
        // Add more scenes as needed
      ],
      "language": "{language}"
    }}

    Edge cases:
    - If there is only one option to branch to, include only that option in "next_scenes".
    - If there are no branching choices, include "branching": {{"decision_point": "exit", "next_scenes": {{}}}}.

    Generate at least 20 scenes with rich interactions and detailed dialogues. Make sure each scene is engaging and educational, providing clear and practical financial literacy lessons.

    Ensure the JSON is valid and complete. Use the following icons in the scenes:

    **Savings**
    - icon11: piggy_bank, https://cdn-icons-png.flaticon.com/512/5488/5488049.png
    - icon12: dollar_sign, https://static.vecteezy.com/system/resources/previews/009/341/093/original/money-icon-dollar-sign-design-free-png.png
    - icon13: Bag with dollar sign, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLgu3mH2ZdXvYKqSMFGrGVIaf9th-It1yswpQm3ZV5gA&s
    - icon14: Bank, https://cdn-icons-png.flaticon.com/512/2830/2830284.png
    - icon15: CPF, https://www.cpf.gov.sg/content/dam/web/member/who-we-are/images/CPF%20Logo_FA-01%20(2).png
    - icon16: Money burning, inflation, https://cdn-icons-png.flaticon.com/512/5068/5068223.png
    - icon17: Budget, https://cdn-icons-png.flaticon.com/512/781/781831.png
    - icon18: Debt, https://cdn-icons-png.flaticon.com/512/3535/3535361.png

    **Insurance**
    - icon21: hand with shield, https://cdn-icons-png.flaticon.com/512/5455/5455507.png
    - icon22: health insurance, https://icons.veryicon.com/png/o/object/warning-icon/health-insurance-1.png
    - icon23: protection from risk, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHzNp_5n2JNhoiZ3BwKrKJFBptXAXJA0K2cw&s
    - icon24: critical illness insurance, https://cdn2.iconfinder.com/data/icons/life-insurance-innovicons-color/128/button-Critical_illness-insurance-hospital-shield-512.png
    - icon25: insurance for property, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLUkKgeetGQrB6CdEMfaMqi31jBf6l2iuC1A&s
    - icon26: personal accident insurance, https://cdn-icons-png.flaticon.com/512/2300/2300379.png
    - icon27: Life insurance, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRI21Nb8VbCFTTuukjlmvNQ8Kwg-3eCybX6TA&s

    **Investment**
    - icon31: hand with positive growth chart, https://cdn-icons-png.flaticon.com/512/4221/4221633.png
    - icon32: Hand with plant-nurturing and growth of investments, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxXtMjfQmv2ZPuIV-ODzcJqWw8r025HCNDtg&s
    - icon33: bonds, https://cdn-icons-png.flaticon.com/512/3776/3776157.png
    - icon34: stock profit, https://cdn-icons-png.flaticon.com/256/6513/6513831.png
    - icon35: Investment Portfolio, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE0PbLkYsSRlHlYxLRQB10xl_aqMnWHwP5HQ&s
    - icon36: Coins Stack, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQATHNwAtdIoA22s7v_EJebfNGsnRByl2CnA2o41v4fDw&s
    - icon37: Buy button, https://cdn-icons-png.flaticon.com/512/600/600231.png
    - icon38: Sell button, https://cdn-icons-png.flaticon.com/512/4106/4106603.png
    - icon39: Calculator, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2REBWhSfmpWv9bGJTPTaJRjIN_901GhUN7Q&s
    - icon391: Low/medium/high risk, https://img.freepik.com/premium-vector/risk-meter-icon-set-scale-low-medium-high-risk-speedometer_349999-1938.jpg

    **Town**
    - icon41: Town, https://cdn.storyboardthat.com/storyboard-creator/thumbs/5201_Large.webp
    - icon42: Town-sun shining, https://cdn.storyboardthat.com/storyboard-creator/thumbs/12306_Large.webp
    - icon43: City in background, https://cdn.storyboardthat.com/storyboard-creator/thumbs/8492_Large.webp

    Here is the information extracted from the link to base the lesson on:
    {json_data}

    Please ensure the lesson is tailored for elderly learners and emphasizes key concepts of financial literacy.
    """
    lesson_json = await generate_lesson_from_text(prompt)
    lesson_data = lesson_json  # since lesson_json is already a dict
    print(lesson_data)

    if not validate_lesson_data(lesson_data):
        raise HTTPException(status_code=400, detail="Invalid lesson data structure")

    lesson = Lesson(**lesson_data)
    new_lesson = await create_lesson(lesson)
    return new_lesson


@router.get("/lessons/", response_model=List[LessonInDB])
async def fetch_lessons():
    lessons = await get_lessons()
    if lessons:
        return lessons
    raise HTTPException(status_code=404, detail="No lessons found")