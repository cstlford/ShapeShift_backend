from flask import Flask, request, jsonify
import enum
from typing import Dict,Any
from gemini_api import generate
app = Flask(__name__)

class Goal(enum.Enum):
    LOSE = 1
    MAINTAIN = 2
    GAIN = 3

class ActivityLevel(enum.Enum):
    SEDENTARY = 1.2
    LIGHTLY_ACTIVE = 1.375
    MODERATELY_ACTIVE = 1.55
    VERY_ACTIVE = 1.725
    EXTRA_ACTIVE = 1.9

class DietType(enum.Enum):
    OMNIVORE = 1
    CARNIVORE = 2
    KETO = 3
    VEGAN = 4
    VEGETARIAN = 5

def calculate_bmr(weight_lbs: float, height_inches: float, age: int, is_male: bool) -> float:
    weight_kg = weight_lbs * 0.453592
    height_cm = height_inches * 2.54
    if is_male:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def calculate_tdee(bmr: float, activity_level: float) -> float:
    return bmr * activity_level

def calculate_target_calories(tdee: float, goal: Goal) -> float:
    if goal == Goal.LOSE:
        return tdee * 0.75  # 75% of TDEE for weight loss
    elif goal == Goal.GAIN:
        return tdee * 1.25  # 125% of TDEE for weight gain
    else:  # MAINTAIN
        return tdee
    
def calculate_macros(target_calories: float, goal: Goal, weight_lbs: float, diet_type: DietType) -> Dict[str, int]:
    if diet_type == DietType.OMNIVORE:
        return calculate_macros_omnivore(target_calories, goal, weight_lbs)
    elif diet_type == DietType.CARNIVORE:
        return calculate_macros_carnivore(target_calories, weight_lbs)
    elif diet_type == DietType.KETO:
        return calculate_macros_keto(target_calories, weight_lbs)
    elif diet_type == DietType.VEGAN:
        return calculate_macros_vegan(target_calories, goal, weight_lbs)
    elif diet_type == DietType.VEGETARIAN:
        return calculate_macros_vegetarian(target_calories, goal, weight_lbs)
    else:
        raise ValueError("Invalid diet type")
    
def calculate_macros_omnivore(target_calories: float, goal: Goal, weight_lbs: float) -> Dict[str, int]:
    if goal == Goal.LOSE:
        protein = weight_lbs  # 1g per lb of body weight
        fat = target_calories * 0.25 / 9
        carbs = (target_calories - (protein * 4 + fat * 9)) / 4
    elif goal == Goal.GAIN:
        protein = weight_lbs * 0.8  # 0.8g per lb of body weight
        fat = target_calories * 0.25 / 9
        carbs = (target_calories - (protein * 4 + fat * 9)) / 4
    else:  # MAINTAIN
        protein = weight_lbs * 0.9  # 0.9g per lb of body weight
        fat = target_calories * 0.3 / 9
        carbs = (target_calories - (protein * 4 + fat * 9)) / 4
    
    return {
        "protein": round(protein),
        "fat": round(fat),
        "carbs": round(carbs)
    }

def calculate_macros_carnivore(target_calories: float, weight_lbs: float) -> Dict[str, int]:
    protein = weight_lbs * 1.2  # Higher protein intake
    fat = (target_calories - (protein * 4)) / 9
    return {
        "protein": round(protein),
        "fat": round(fat),
        "carbs": 0  # Carnivore diet typically excludes carbs
    }

def calculate_macros_keto(target_calories: float, weight_lbs: float) -> Dict[str, int]:
    fat = target_calories * 0.75 / 9  # 75% of calories from fat
    protein = weight_lbs  # 1g per lb of body weight
    carbs = (target_calories - (fat * 9 + protein * 4)) / 4
    return {
        "protein": round(protein),
        "fat": round(fat),
        "carbs": round(carbs)
    }

def calculate_macros_vegan(target_calories: float, goal: Goal, weight_lbs: float) -> Dict[str, int]:
    if goal == Goal.LOSE:
        protein = weight_lbs * 0.8  # Slightly lower protein, plant-based sources
        fat = target_calories * 0.25 / 9
    elif goal == Goal.GAIN:
        protein = weight_lbs * 0.7
        fat = target_calories * 0.3 / 9
    else:  # MAINTAIN
        protein = weight_lbs * 0.75
        fat = target_calories * 0.28 / 9
    
    carbs = (target_calories - (protein * 4 + fat * 9)) / 4
    return {
        "protein": round(protein),
        "fat": round(fat),
        "carbs": round(carbs)
    }

def calculate_macros_vegetarian(target_calories: float, goal: Goal, weight_lbs: float) -> Dict[str, int]:
    if goal == Goal.LOSE:
        protein = weight_lbs * 0.9  # Slightly higher than vegan
        fat = target_calories * 0.25 / 9
    elif goal == Goal.GAIN:
        protein = weight_lbs * 0.8
        fat = target_calories * 0.3 / 9
    else:  # MAINTAIN
        protein = weight_lbs * 0.85
        fat = target_calories * 0.28 / 9
    
    carbs = (target_calories - (protein * 4 + fat * 9)) / 4
    return {
        "protein": round(protein),
        "fat": round(fat),
        "carbs": round(carbs)
    }

def nutrition_plan(
    weight_lbs: float, 
    height_inches: float, 
    age: int, 
    is_male: bool, 
    goal: Goal,
    diet_type: DietType,
    activity_level: ActivityLevel,
   
) -> Dict[str, Any]:
    bmr = calculate_bmr(weight_lbs, height_inches, age, is_male)
    tdee = calculate_tdee(bmr, activity_level.value)
    target_calories = calculate_target_calories(tdee, goal)
    macros = calculate_macros(target_calories, goal, weight_lbs, diet_type)
    
    return {
        "target_calories": round(target_calories),
        "macros": macros,
    }

@app.route('/nutrition_plan', methods=['POST'])
def get_nutrition_plan():
        data = request.json
        try:
            weight_lbs = float(data['weight_lbs'])
            height_inches = float(data['height_inches'])
            age = int(data['age'])
            is_male = bool(data['is_male'])
            goal = Goal[data['goal'].upper()]
            diet_type = DietType[data['diet_type'].upper()]
            activity_level = ActivityLevel[data['activity_level'].upper()]
            #returns dictionary with calories and macros 
            plan = nutrition_plan(
                weight_lbs, height_inches, age, is_male, goal, diet_type,
                activity_level
            )
        except KeyError as e:
            return jsonify({"error": f"Missing required field: {str(e)}"}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        #returns LLM output based on 'plan' (macros and calories)
        return generate(plan)


if __name__ == '__main__':
    app.run(debug=True)