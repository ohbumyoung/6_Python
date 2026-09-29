"""
    환경 설정 확인
    (실습 시작 시 실행하여 결과를 확인)

    1. 패키지 확인
    2. .env 파일 (파일 존재, 설정 항목 여부)
    3. 오라클 접속
    4. 문자셋 확인
    5. 권한 (테이블 생성, 삭제)
"""
import os

def step1_packages():
    """ 패키지 설치 여부 확인 """
    need = {
        "oracleb" : "Oracle 드라이버",
        "sqlalchemy" : "DB 추상화 계층 (Pandas 연동)",
        "dotenv" : "환경 변수 로딩",
        "pandas" : "데이터 처리",
        "requests" : "API 호출"
    }

    missing = []
    for mod, desc in need.items():
        try:
            m = __import__(mod)
            ver = getattr(m, '__version__', '')
            print(f"[OK] {mod:<14}{ver:<12}{desc}")
        except ImportError:
            print(f"[실패] {mod:<14}{'':<12}{desc}")
            missing.append(mod)

    if missing:
        raise RuntimeError(
            f"설치되지 않은 항목 : {missing}\n"
            " 해결 : ,pip install -r requirements.txt\n"
            " requirements.txt 파일이 없는 경우, 직접 설치\n"
            f" 해결:pip install oracle sqlalchemy dotenv pandas requests"
        )

    def step2_env():
        """ .enb 파일 확인"""
        from dotenv import load_dotenv

        if not os.path.exists(".env"):
            raise FileNotFoundError(
                ".env 파일이 없습니다.\n"
                " 해결: copy .env.example .env\n"
                " 그 다음 설정 항목에 값을 채워주세요"
            )

        load_dotenv()
        
        required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]

        for key in required:
            value = os.getenv(key)

            if not value:
                raise ValueError(f"{key} 가 비어 있습니다.")

            show = "*"*len(value) if "PASSWORD" in key else value
            print(f"[OK] {key:<14} {show}")

        if "write" in os.getenv("DB_PASSWORD", ""):
            raise ValueError("DB_PASSWORD 가 예시 그대로입니다.\n" \
            ".env 파일을 열어 값을 변경해주세요.")

    # .gitignore : 깃에서 관리하지 않을 항목 관리하는 파일
    for gitign in (".gitignore", os.path.join("..", ".gitignore")):
        if os.path.exists(gitign):
            with open(gitign, encoding="UTF-8") as f:
                if ".env" in f.read():
                    print(f"[OK] .gitignore에 .env파일이 등록됨 ({gitign})")
                else:
                    print(f"[실패] {gitign} 에 .env 파일이 없음! 추가 필요!")
            break
        else:
            # for문이 break없이 끝났을 때 실행되는 부분! => 제시한 경로에서 파일을 찾지 못했을 때
            print(f"[실패] .gitignore 파일을 찾지 못했습니다. 파일을 추가해주세요.")

def step3_connect():
    """ 오라클 접속 확인 """
    import oracledb
    from dotenv import load_dotenv

    load_dotenv()
    try:
        conn = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn=f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    except oracledb.Error as e:
        err_obj, = e.args
        code = err_obj.code

        message = {
            1017: "비밀번호나 사용자명이 잘못되었습니다. .env 파일을 확인하세요구르트.",
            12154: "접속 식별자를 해석하지 못했습니다. HOST, NAME을 확인하세요를레히",
            12541: "TNS 리스너가 없습니다. 포트 번호, 서버 실행 여부를 확인하세요리사"
        }.get(code, "해당 코드를 관리자에게 문의하세요단강.(검색)")

        raise RuntimeError(f"{e}\n --> {message}")
    except UnicodeEncodeError:
        # 비밀번호에 한글이 포함된 경우 해당 예외가 발생
        raise RuntimeError(
            "접속 정보에 한글이 포함되어 있습니다.\n"
            "--> DB 비밀번호, 사용자명은 영문, 숫자, 기호만으로만 사용해주세요"
        )