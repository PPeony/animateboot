from ytmusicapi import YTMusic

# 初始化 (不需要 API 密钥)
ytmusic = YTMusic()


def search_in_youtube(search_query):
    if search_query is None:
        return None
    # else:
    #     return {"title":search_query,"videoId":"a"}
    # 搜索歌曲
    # search_query = "「Majestic Catastrophe」佐佐木李子"
    search_results = ytmusic.search(search_query)

    # 打印返回的匹配结果
    # 结果是一个列表，包含了字典，每个字典代表一个结果
    # 结果类型可能包括 'song', 'video', 'album', 'artist', 'playlist'

    print(f"--- 正在搜索: '{search_query}' ---")

    if not search_results:
        print("没有找到结果。")
    else:
        # 通常第一个 'song' 类型的结果是最佳匹配
        for item in search_results:
            if item['resultType'] == 'song':
                print(f"类型: {item['resultType']}")
                print(f"歌曲: {item['title']}")
                print(f"艺术家: {', '.join([artist['name'] for artist in item['artists']])}")
                print(f"Video ID: {item['videoId']}")  # 这是 YouTube 视频 ID
                print(f"时长: {item['duration']}")
                print("------------------------------")
                # 找到第一个歌曲结果后就停止，或继续遍历所有结果
                res = {"title": item['title'], "videoId": item['videoId'], "resultType": item['resultType']}
                return res
    return None
