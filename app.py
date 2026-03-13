import streamlit as st
import urllib.parse
import requests
 
# ─── 페이지 설정 ───────────────────────────────────────────
st.set_page_config(
    page_title="삼돌이 블로그 수호 센터",
    page_icon="🚨",
    layout="centered"
)
 
# ─── 스타일 ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
 
.result-box {
    padding: 18px 22px;
    border-radius: 12px;
    margin: 12px 0;
    font-size: 15px;
    line-height: 1.7;
}
.result-safe   { background: #e8f5e9; border-left: 5px solid #2e7d32; color: #1b5e20; }
.result-danger { background: #ffebee; border-left: 5px solid #c62828; color: #7f0000; }
.result-warn   { background: #fff8e1; border-left: 5px solid #f57f17; color: #6d4c00; }
 
.big-status {
    font-size: 28px;
    font-weight: 900;
    text-align: center;
    padding: 24px;
    border-radius: 16px;
    margin: 16px 0;
}
.status-ok     { background: #e8f5e9; color: #2e7d32; }
.status-danger { background: #ffebee; color: #c62828; }
.status-warn   { background: #fff8e1; color: #e65100; }
</style>
""", unsafe_allow_html=True)
 
# ─── API 키 로드 ───────────────────────────────────────────
try:
    NAVER_CLIENT_ID     = st.secrets["NAVER_CLIENT_ID"]
    NAVER_CLIENT_SECRET = st.secrets["NAVER_CLIENT_SECRET"]
    naver_ok = True
except:
    naver_ok = False
 
if not naver_ok:
    st.error("⚠️ 네이버 API 키가 설정되지 않았습니다. Streamlit Secrets에 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 추가해주세요.")
 
# ─── 검색 함수 ─────────────────────────────────────────────
def naver_search(query, search_type="webkr", display=10):
    if not naver_ok:
        return None
    url = f"https://openapi.naver.com/v1/search/{search_type}.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    try:
        res = requests.get(url, headers=headers, params={"query": query, "display": display}, timeout=10)
        return res.json() if res.status_code == 200 else None
    except:
        return None
 
def naver_blog_search(query, display=10):
    if not naver_ok:
        return None
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    try:
        res = requests.get(url, headers=headers, params={"query": query, "display": display}, timeout=10)
        return res.json() if res.status_code == 200 else None
    except:
        return None
 
# ─── 헤더 ──────────────────────────────────────────────────
st.title("🚨 삼돌이 블로그 수호 센터")
st.write("불펌 감지와 누락 확인을 한 번에 해결하세요!")
 
tab1, tab2 = st.tabs(["🕵️ 불펌 감지기", "📉 누락 확인기"])
 
# ════════════════════════════════════════════════════════════
# 탭 1: 불펌 감지기
# ════════════════════════════════════════════════════════════
with tab1:
    st.header("내 글 무단 도용 추적")
    st.write("내 글의 고유한 문장을 입력하면 네이버에서 동일/유사 글을 찾아드려요.")
 
    my_text     = st.text_area("내 글에서 가장 고유한 문장을 입력하세요",
                               placeholder="예: 오늘은 제가 직접 김포에서 먹어본 찐 맛집 후기를 남겨봅니다.",
                               height=120)
    search_blog = st.checkbox("블로그도 함께 검색", value=True)
 
    if st.button("🚨 도둑놈 추적 시작", type="primary", use_container_width=True):
        if not my_text.strip():
            st.warning("⚠️ 문장을 입력해주세요!")
        else:
            with st.spinner("🔍 네이버 검색 중..."):
                web_data  = naver_search(f'"{my_text.strip()}"', "webkr", 5)
                blog_data = naver_blog_search(f'"{my_text.strip()}"', 5) if search_blog else None
 
            st.subheader("📊 검색 결과 분석")
            total_found = 0
 
            if web_data is not None:
                web_total = web_data.get("total", 0)
                total_found += web_total
                if web_total == 0:
                    st.markdown('<div class="result-box result-safe">✅ <b>웹 전체:</b> 동일 문장 발견되지 않음</div>', unsafe_allow_html=True)
                elif web_total <= 2:
                    st.markdown(f'<div class="result-box result-warn">⚠️ <b>웹 전체:</b> {web_total}건 발견 — 확인 필요</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-box result-danger">🚨 <b>웹 전체:</b> {web_total}건 발견 — 무단 도용 의심!</div>', unsafe_allow_html=True)
                for item in web_data.get("items", []):
                    title = item.get("title","").replace("<b>","").replace("</b>","")
                    st.markdown(f"- [{title}]({item.get('link','')})")
 
            if blog_data is not None:
                blog_total = blog_data.get("total", 0)
                total_found += blog_total
                if blog_total == 0:
                    st.markdown('<div class="result-box result-safe">✅ <b>블로그:</b> 동일 문장 발견되지 않음</div>', unsafe_allow_html=True)
                elif blog_total <= 2:
                    st.markdown(f'<div class="result-box result-warn">⚠️ <b>블로그:</b> {blog_total}건 발견 — 확인 필요</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-box result-danger">🚨 <b>블로그:</b> {blog_total}건 발견 — 무단 도용 의심!</div>', unsafe_allow_html=True)
                for item in blog_data.get("items", []):
                    title = item.get("title","").replace("<b>","").replace("</b>","")
                    st.markdown(f"- [{title}]({item.get('link','')}) — {item.get('bloggername','')}")
 
            st.subheader("🏁 종합 판단")
            if total_found == 0:
                st.markdown('<div class="big-status status-ok">✅ 도용 없음<br><small style="font-size:16px;font-weight:400;">동일 문장이 발견되지 않았습니다</small></div>', unsafe_allow_html=True)
            elif total_found <= 3:
                st.markdown(f'<div class="big-status status-warn">⚠️ 확인 필요<br><small style="font-size:16px;font-weight:400;">총 {total_found}건 — 직접 확인해보세요</small></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="big-status status-danger">🚨 도용 의심<br><small style="font-size:16px;font-weight:400;">총 {total_found}건 발견 — 즉시 확인 필요!</small></div>', unsafe_allow_html=True)
 
            naver_url = f"https://search.naver.com/search.naver?query={urllib.parse.quote(chr(34) + my_text.strip() + chr(34))}"
            st.link_button("👉 네이버에서 직접 확인하기", naver_url, use_container_width=True)
 
# ════════════════════════════════════════════════════════════
# 탭 2: 누락 확인기
# ════════════════════════════════════════════════════════════
with tab2:
    st.header("포스팅 누락(미노출) 체크")
    st.write("블로그 포스팅 URL 또는 제목으로 네이버 노출 여부를 확인해요.")
 
    check_mode  = st.radio("확인 방식", ["URL로 확인", "제목으로 확인"], horizontal=True)
    check_input = st.text_input(
        "포스팅 URL을 입력하세요" if check_mode == "URL로 확인" else "포스팅 제목을 입력하세요",
        placeholder="https://blog.naver.com/xxx/포스팅번호" if check_mode == "URL로 확인" else "예: 김포 맛집 추천 TOP5"
    )
 
    if st.button("🔍 누락 확인 시작", type="primary", use_container_width=True):
        if not check_input.strip():
            st.warning("⚠️ URL 또는 제목을 입력해주세요!")
        else:
            with st.spinner("🔍 네이버 노출 여부 확인 중..."):
 
                if check_mode == "URL로 확인":
                    data = naver_search(f"site:{check_input.strip()}", "webkr", 3)
                    st.subheader("📊 색인(등록) 여부 확인")
                    if data is not None:
                        if data.get("total", 0) > 0:
                            st.markdown('<div class="big-status status-ok">✅ 노출 중<br><small style="font-size:16px;font-weight:400;">네이버에 정상 등록된 포스팅입니다</small></div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="big-status status-danger">❌ 누락됨<br><small style="font-size:16px;font-weight:400;">네이버에서 찾을 수 없습니다</small></div>', unsafe_allow_html=True)
                            st.markdown("""<div class="result-box result-danger">
❌ 이 포스팅이 네이버에 노출되지 않고 있습니다.<br><br>
<b>가능한 원인:</b><br>
• 발행한 지 얼마 안 됨 (보통 1~3일 소요)<br>
• 저품질 블로그로 분류됨<br>
• 중복 콘텐츠로 판단됨
</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="result-box result-warn">⚠️ 확인 중 오류가 발생했습니다. 아래 버튼으로 직접 확인해주세요.</div>', unsafe_allow_html=True)
 
                    st.link_button("👉 네이버에서 직접 확인하기",
                                   f"https://search.naver.com/search.naver?query={urllib.parse.quote('site:' + check_input.strip())}",
                                   use_container_width=True)
 
                else:
                    blog_data  = naver_blog_search(check_input.strip(), 5)
                    web_data   = naver_search(check_input.strip(), "webkr", 5)
                    blog_found = any(check_input.strip()[:10] in item.get("title","").replace("<b>","").replace("</b>","")
                                     for item in (blog_data or {}).get("items", []))
                    web_found  = any(check_input.strip()[:10] in item.get("title","").replace("<b>","").replace("</b>","")
                                     for item in (web_data or {}).get("items", []))
 
                    st.subheader("📊 제목 노출 여부 확인")
                    if blog_found or web_found:
                        st.markdown('<div class="big-status status-ok">✅ 노출 중<br><small style="font-size:16px;font-weight:400;">해당 제목의 글이 네이버에 노출됩니다</small></div>', unsafe_allow_html=True)
                        if blog_found:
                            st.markdown('<div class="result-box result-safe">✅ 블로그 검색에서 발견되었습니다.</div>', unsafe_allow_html=True)
                        if web_found:
                            st.markdown('<div class="result-box result-safe">✅ 웹 검색에서 발견되었습니다.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="big-status status-danger">❌ 누락 의심<br><small style="font-size:16px;font-weight:400;">해당 제목이 검색되지 않습니다</small></div>', unsafe_allow_html=True)
                        st.markdown("""<div class="result-box result-danger">
❌ 해당 제목의 글이 네이버 검색에 나타나지 않습니다.<br><br>
<b>확인해보세요:</b><br>
• 제목을 정확하게 입력하셨나요?<br>
• 발행 후 1~3일이 지났나요?<br>
• 블로그 공개 설정이 되어 있나요?
</div>""", unsafe_allow_html=True)
 
                    st.link_button("👉 네이버에서 직접 확인하기",
                                   f"https://search.naver.com/search.naver?query={urllib.parse.quote(check_input.strip())}",
                                   use_container_width=True)
 
# ─── 푸터 ──────────────────────────────────────────────────
st.divider()
st.caption("© 2024 삼돌이군의 블로그 로봇. 모든 권리는 대장님께 있습니다.")
 




네이버 검색키워드 API 단가/난이도 기능 오류 - Claude
