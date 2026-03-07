import streamlit as st
import urllib.parse

# 1. 페이지 설정
st.set_page_config(page_title="도둑놈 잡는 삼돌이", page_icon="🚨")

st.title("🚨 삼돌이 블로그 수호 센터")
st.write("불펌 감지와 누락 확인을 한 번에 해결하세요!")

# 탭 메뉴 만들기 (불펌 감지 / 누락 확인)
tab1, tab2 = st.tabs(["🕵️ 불펌 감지기", "📉 누락 확인기"])

# --- 탭 1: 불펌 감지기 ---
with tab1:
    st.header("내 글 무단 도용 추적")
    my_post_text = st.text_area("내 글에서 가장 고유한 문장을 넣어주세요.", 
                               placeholder="예: 오늘은 제가 직접 김포에서 먹어본 찐 맛집 후기를 남겨봅니다.")
    
    if st.button("🚨 도둑놈 추적 시작"):
        if not my_post_text:
            st.warning("⚠️ 문장을 입력해주세요!")
        else:
            search_query = f'"{my_post_text}"'
            encoded_query = urllib.parse.quote(search_query)
            naver_url = f"https://search.naver.com/search.naver?query={encoded_query}"
            st.success("✅ 추적 경로 확보!")
            st.link_button("👉 네이버 결과 확인 (클릭)", naver_url)

# --- 탭 2: 누락 확인기 ---
with tab2:
    st.header("포스팅 누락(미노출) 체크")
    check_url = st.text_input("확인할 포스팅 주소를 넣어주세요.")
    
    if st.button("🔍 누락 확인 시작"):
        if not check_url:
            st.warning("⚠️ 주소를 입력해주세요!")
        else:
            # 색인 확인 (site: 검색)
            site_query = f"site:{check_url}"
            site_link = f"https://search.naver.com/search.naver?query={urllib.parse.quote(site_query)}"
            
            st.success("✅ 확인 경로 생성!")
            st.link_button("👉 네이버 등록 여부 확인 (클릭)", site_link)
            st.info("💡 위 버튼을 눌렀는데 결과가 '0건'이면 누락된 것입니다!")

st.divider()
st.caption("© 2024 삼돌이군의 블로그 로봇. 모든 권리는 대장님께 있습니다.")