import time
import getpass
from typing import List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


NAVER_HOME = "https://www.naver.com/"
NAVER_LOGIN = "https://nid.naver.com/nidlogin.login"
# KBS(oid=056)
KBS_NEWS_LIST = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=056"


def make_driver(headless: bool = False) -> webdriver.Chrome:
    """Selenium 4.6+ : Selenium Manager로 드라이버 자동 관리."""
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    # 안정성 옵션
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,1800")
    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(30)
    return driver


def before_login_snapshot(driver: webdriver.Chrome) -> None:
    """로그인 전 스냅샷(화면 캡처) 저장 및 대표 영역 존재 여부 출력."""
    driver.get(NAVER_HOME)
    time.sleep(1.0)
    driver.save_screenshot("pre_login.png")
    # 로그인 영역 존재 여부 확인(버튼/링크 텍스트 등 다소 관대한 탐색)
    try:
        login_btn = driver.find_elements(
            By.XPATH, "//a[contains(@href,'nidlogin') or contains(text(),'로그인')]")
        print(f"[INFO] 로그인 전: 로그인 진입 링크/버튼 추정 개수 = {len(login_btn)}")
    except Exception:
        print("[INFO] 로그인 전: 로그인 요소 탐색 실패(무시)")


def login_naver(driver: webdriver.Chrome, user_id: str, user_pw: str) -> bool:
    """아이디/비밀번호 입력 후 로그인 시도."""
    driver.get(NAVER_LOGIN)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "id")))
    except TimeoutException:
        print("[ERROR] 로그인 페이지 로드 지연")
        return False

    # 입력 및 전송
    id_input = driver.find_element(By.ID, "id")
    pw_input = driver.find_element(By.ID, "pw")
    id_input.clear()
    id_input.send_keys(user_id)
    pw_input.clear()
    pw_input.send_keys(user_pw)

    # 로그인 버튼: 페이지에 따라 id/name/aria-label이 다를 수 있어 여러 후보 시도
    clicked = False
    for locator in [
        (By.ID, "log.login"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input.btn_login"),
        (By.XPATH,
         "//button[contains(.,'로그인') or contains(@aria-label,'로그인')]"),
    ]:
        try:
            driver.find_element(*locator).click()
            clicked = True
            break
        except NoSuchElementException:
            continue

    if not clicked:
        print("[ERROR] 로그인 버튼을 찾지 못했습니다.")
        return False

    # 홈으로 이동(일부 환경에서 보안단계/추가인증이 있을 수 있음)
    try:
        WebDriverWait(driver, 20).until(EC.url_contains("naver.com"))
    except TimeoutException:
        # 추가 인증 화면일 수 있으니 캡처만 남기고 실패 처리
        driver.save_screenshot("post_login_maybe_blocked.png")
        print("[WARN] 추가 인증/보안절차 감지. 수동 인증 후 다시 실행하세요.")
        return False

    return True


def after_login_snapshot(driver: webdriver.Chrome) -> None:
    """로그인 후 스냅샷 저장 및 사용자 영역 존재 여부 출력."""
    driver.get(NAVER_HOME)
    time.sleep(1.0)
    driver.save_screenshot("post_login.png")
    # 사용자 영역(알림/프로필 등) 유무 대략 확인
    try:
        # 로그인 후에만 보일법한 '내정보/프로필' 유사 텍스트 탐색(관대)
        user_elems = driver.find_elements(
            By.XPATH,
            "//*[contains(text(),'내정보') or contains(text(),'프로필') or contains(@aria-label,'내정보')]",
        )
        print(f"[INFO] 로그인 후: 사용자 영역 추정 개수 = {len(user_elems)}")
    except Exception:
        print("[INFO] 로그인 후: 사용자 요소 탐색 실패(무시)")


def fetch_kbs_headlines(driver: webdriver.Chrome, limit: int = 20) -> List[Tuple[str, str]]:
    """
    KBS 기사 제목/링크 수집.
    네이버 뉴스 리스트(press=KBS) 페이지에서 a 태그 수집 후 정제.
    """
    driver.get(KBS_NEWS_LIST)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "main_content")))
    except TimeoutException:
        print("[ERROR] KBS 뉴스 목록 로드 실패")
        return []

    anchors = driver.find_elements(By.CSS_SELECTOR, "#main_content a")
    seen = set()
    items: List[Tuple[str, str]] = []
    for a in anchors:
        title = (a.text or "").strip()
        href = a.get_attribute("href") or ""
        # 제목이 있고 기사 링크처럼 보이는 것만 통과
        if title and "read.naver" in href:
            key = (title, href)
            if key not in seen:
                seen.add(key)
                items.append((title, href))
                if len(items) >= limit:
                    break

    return items


def main() -> None:
    print("=== 네이버 로그인 전/후 비교 + KBS 기사 크롤링 ===")
    # 자격 증명 입력(비밀번호는 콘솔에 표시되지 않음)
    user_id = input("NAVER ID : ").strip()
    user_pw = getpass.getpass("NAVER PW : ")

    driver = make_driver(headless=False)
    try:
        # 1) 로그인 전
        before_login_snapshot(driver)

        # 2) 로그인
        ok = login_naver(driver, user_id, user_pw)
        if not ok:
            print("[FAIL] 로그인 실패. (추가 인증이 걸린 경우 수동 인증 후 재시도)")
            return

        # 3) 로그인 후
        after_login_snapshot(driver)

        # 4) KBS 기사 크롤링
        kbs_list = fetch_kbs_headlines(driver, limit=30)

        # 5) 리스트에 담아 전체 출력
        print("\n[KBS 최신 기사 목록]")
        for idx, (title, url) in enumerate(kbs_list, start=1):
            print(f"{idx:02d}. {title} | {url}")

        if not kbs_list:
            print("[INFO] 수집된 기사가 없습니다. (페이지 구조 변경/접속 이슈 가능)")

    finally:
        # 리소스 정리
        time.sleep(1.0)
        driver.quit()


if __name__ == "__main__":
    main()
