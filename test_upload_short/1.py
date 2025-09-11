import re

def ends_with_tag(text: str) -> bool:
    text = text.strip()
    return bool(re.search(r"(?:^|\s)(#[\w]+)$", text))

# Ví dụ:
s1 = "⚡🌟 Miniature food & fruits ASMR Sound Review 🤯 #cooker #cookingtoys #ricecooker #kitchentoys"
s2 = "Miniature ASMR review 🤯"
s3 = "This ends with #tag"

print(ends_with_tag(s1))  # True
print(ends_with_tag(s2))  # False
print(ends_with_tag(s3))  # True
