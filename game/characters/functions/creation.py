import random
import json
import os
from typing import List, Dict, Optional
from llm.ai21 import LLMServiceAI21
from config import PARAM_NAMES, MORAL_POOL


class Character:
    def __init__(self, name: str, params: Dict[str, int], legend: str, morals: Dict[str, str], mood: float = 0.5, position: Optional[tuple] = None, memory: Optional[str] = None, relations: Optional[Dict] = None):
        self.name = name
        self.params = params
        self.legend = legend
        self.morals = morals
        self.mood = mood
        self.position = position
        self.relations = relations if relations is not None else {}
        self.memory = memory if memory is not None else []

    def load_memory(self, memory_file: str) -> List[str]:
        try:
            with open(memory_file, 'r', encoding='utf-8') as file:
                return json.load(file).get('memory', [])
        except Exception as e:
            print(f"Ошибка при загрузке памяти: {e}")
        return []

    def save_memory(self, memory_file: str):
        if not os.path.exists(os.path.dirname(memory_file)):
            os.makedirs(os.path.dirname(memory_file), exist_ok=True)

        with open(memory_file, 'w', encoding='utf-8') as file:
            json.dump({'memory': self.memory}, file, ensure_ascii=False, indent=4)

    def add_memory(self, new_memories: List[str]):
        self.memory.extend(new_memories)
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]
        self.save_memory(f"memory/{self.name}.json")

    def save_to_json(self, directory="/Users/masterpo/Desktop/MicroWorld/characters/"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, f"{self.name}.json")
        data = {
            "name": self.name,
            "params": self.params,
            "legend": self.legend,
            "morals": self.morals,
            "relations": self.relations,
            "memory": self.memory,
            "mood": self.mood
        }

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Персонаж сохранён в файл: {file_path}")



class CreateCharacter:
    def __init__(self, total_points: int = 50, param_names: Optional[List[str]] = None, moral_pool: Optional[List[Dict[str, str]]] = None):
        self.total_points = total_points
        self.param_names = param_names or PARAM_NAMES
        self.moral_pool = moral_pool or MORAL_POOL

    def generate_balanced_params(self) -> Dict[str, int]:
        params = {name: 1 for name in self.param_names}
        remaining_points = self.total_points - len(self.param_names)

        while remaining_points > 0:
            param = random.choice(self.param_names)
            if params[param] < 10:
                params[param] += 1
                remaining_points -= 1
        return params

    def generate_moral_principles(self) -> Dict[str, str]:
        selected_principles = random.sample(self.moral_pool, random.randint(2, 5))
        return {principle["key"]: principle["description"] for principle in selected_principles}

    def generate_legend_with_llm(self, name: str, params: Dict[str, int], morals: Dict[str, str]) -> str:
        system_message = "You are a creative writer who generates unique and immersive backstories for fantasy characters."
        user_message = (
            f"Create a legend for a character named {name}. The character's attributes are: "
            + ", ".join([f"{key} {value}" for key, value in params.items()])
            + ". The character's moral principles are: "
            + ", ".join(morals.values())
            + ". The legend should explain the origin of their values, motivations, and goals."
        )
        giga = LLMServiceAI21()
        return giga.generate_response(system_message, user_message)

    def generate_character(self, name: str) -> Character:
        params = self.generate_balanced_params()
        moral_principles = self.generate_moral_principles()
        legend = self.generate_legend_with_llm(name, params, moral_principles)
        return Character(name, params, legend, moral_principles)
