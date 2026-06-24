import json
import re

transcript_path = r"C:\Users\ayber\.gemini\antigravity\brain\a8d2360f-c0b3-4e2f-a39d-6893c9b5cf9c\.system_generated\logs\transcript_full.jsonl"
merged_data = []
seen_ids = set()

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            # The system messages from subagents appear in the transcript.
            # They might be in type="SYSTEM_MESSAGE" or type="SYSTEM" or inside the content
            # Let's just string match on the raw line to be safe, or parse the content if it exists
            content = data.get("content", "")
            if not content and "step" in data:
                 content = str(data)
                 
            if "```json" in content:
                # extract json block
                matches = re.finditer(r"```json\s*(\[\s*\{.*?\}\s*\])\s*```", content, re.DOTALL)
                for match in matches:
                    json_str = match.group(1)
                    try:
                        parsed = json.loads(json_str)
                        for item in parsed:
                            if "id" in item and item["id"] not in seen_ids:
                                seen_ids.add(item["id"])
                                merged_data.append(item)
                    except Exception as e:
                        pass
        except Exception:
            pass

print(f"Total unique records found: {len(merged_data)}")

final_output = {
    "country_meta": {
        "name": "Italy",
        "currency": "EUR",
        "visa_difficulty": "high",
        "bureaucracy_level": "very_high",
        "general_tuition_model": "ISEE/Income-based with regional DSU scholarships",
        "part_time_work_opportunities": "low_to_medium",
        "post_graduation_visa_years": 1,
        "language_requirement_for_life": "Italian A2/B1 highly recommended"
    },
    "universities": merged_data
}

with open(r"c:\Users\ayber\Desktop\Custom Apps\UniRank\data_base\italy.json", "w", encoding='utf-8') as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)

print("Saved data_base/italy.json")
