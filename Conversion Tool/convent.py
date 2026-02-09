import json
import os

def txt_to_multi_turn_json(txt_file_path, json_file_path=None):
    """
    将包含多轮q:/a:格式的txt文件转换为大模型微调用的JSON对话数据集
    适配Windows系统，支持多轮对话，用空行分隔不同的对话会话
    
    Args:
        txt_file_path: 输入的txt文件路径
        json_file_path: 输出的json文件路径，默认为txt文件同目录同名的json文件
    """
    if json_file_path is None:
        json_file_path = os.path.splitext(txt_file_path)[0] + ".json"
    
    # 存储最终的多轮对话数据集
    dataset = []
    # 临时存储当前的多轮对话（一个完整的多轮会话）
    current_conversation = {"messages": []}
    
    try:
        # 读取txt文件（处理Windows BOM头）
        with open(txt_file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        
        print(f"🔍 成功读取文件，共 {len(lines)} 行内容")
        
        for line_num, line in enumerate(lines, 1):
            # 去除首尾空白字符
            line = line.strip()
            
            # 空行：表示当前多轮对话结束，开始新的对话
            if not line:
                # 如果当前对话有内容，就加入数据集
                if current_conversation["messages"]:
                    dataset.append(current_conversation)
                    print(f"✅ 第{line_num}行：空行分隔，完成一个多轮对话会话（共{len(current_conversation['messages'])}轮）")
                    # 重置临时对话
                    current_conversation = {"messages": []}
                continue
            
            # 处理用户提问（q:）
            if line.startswith('q:'):
                content = line[2:].strip()
                if content:
                    print(f"ℹ️  第{line_num}行：识别到user -> {content}")
                    current_conversation["messages"].append({
                        "role": "user",
                        "content": content
                    })
                else:
                    print(f"⚠️  第{line_num}行：q:后无内容，跳过")
            
            # 处理助手回答（a:）
            elif line.startswith('a:'):
                content = line[2:].strip()
                if content:
                    print(f"ℹ️  第{line_num}行：识别到assistant -> {content}")
                    current_conversation["messages"].append({
                        "role": "assistant",
                        "content": content
                    })
                else:
                    print(f"⚠️  第{line_num}行：a:后无内容，跳过")
            
            # 无效格式
            else:
                print(f"⚠️  第{line_num}行：格式错误（非q:/a:开头），跳过 -> {line}")
        
        # 处理文件末尾未结束的多轮对话
        if current_conversation["messages"]:
            dataset.append(current_conversation)
            print(f"✅ 文件末尾：完成最后一个多轮对话会话（共{len(current_conversation['messages'])}轮）")
        
        # 保存JSON文件
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        # 输出统计信息
        print("\n🎉 转换完成！")
        print(f"📄 输入文件: {txt_file_path}")
        print(f"📄 输出文件: {json_file_path}")
        print(f"📊 共生成 {len(dataset)} 个多轮对话会话")
        
        # 统计总轮次
        total_turns = sum(len(conv["messages"]) for conv in dataset)
        print(f"📈 总对话轮次: {total_turns}")
        
        return json_file_path
    
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {txt_file_path}")
    except UnicodeDecodeError:
        print(f"❌ 错误：文件编码不是UTF-8，请将txt另存为UTF-8格式")
    except Exception as e:
        print(f"❌ 未知错误：{str(e)}")

# 执行入口（Windows适配）
if __name__ == "__main__":
    # 替换为你的txt文件路径（多轮对话格式）
    # 方式1：相对路径（txt和脚本同目录）
    input_txt_path = "dialogueCollection.txt"
    # 方式2：绝对路径示例
    # input_txt_path = "C:\\Users\\小蓝\\Desktop\\connent\\multi_turn_dialogues.txt"
    
    # 执行转换
    txt_to_multi_turn_json(input_txt_path)
    
    # 防止窗口关闭
    input("\n按回车键退出...")