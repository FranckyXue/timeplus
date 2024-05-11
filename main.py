import requests
from docx import Document


def read_rules(file_path):
    """使用python-docx库读取Word文档内容。"""
    doc = Document(file_path)
    rules = []
    for para in doc.paragraphs:
        rules.append(para.text)
    return "\n".join(rules)

def call_chatgpt(user_input, rules, api_key):
    """调用OpenAI的ChatGPT API并返回响应。将用户输入和文档规则结合起来作为输入。"""
    prompt = f"{user_input} 这是一个名叫timeplus的公司的sql规则，我希望你阅读文档中的规则后，在我给我问题后可以为我生成相应的sql语句。下面是关于sql的规则文档:\n{rules}"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-turbo",  # 确保模型名称正确
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()  # 返回JSON数据
    else:
        print(f"Error: {response.status_code} - {response.text}")  # 打印错误信息
        return None  # 明确返回None表示失败

def main():
    """主函数，用于运行程序。"""
    api_key = ""  # 替换为您的API密钥
    rules_path = r"C:\Users\10409\Desktop\Timeplus.docx"  # 指定规则文件的路径
    rules = read_rules(rules_path)
    print("Loaded Rules")  # 为了调试可以打印规则内容
    # print(rules)

    while True:
        user_input = input("Ask me something: ")
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        response = call_chatgpt(user_input, rules, api_key)
        if response and 'choices' in response:
            print("Response from GPT-4:", response['choices'][0]['message']['content'])
        else:
            print("No response or error occurred.")

if __name__ == "__main__":
    main()