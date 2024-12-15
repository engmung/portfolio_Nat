-- 3D 모델링 관련 상세 내용
UPDATE knowledge_items 
SET content = '3D 모델링은 컴퓨터 그래픽스를 사용하여 3차원 공간에서 물체를 만들고 조작하는 과정입니다. 여기에는 폴리곤 모델링, NURBS 모델링, 스컬프팅 등 다양한 기법이 포함됩니다.'
WHERE id = 1;

-- 기초모델링 상세 내용
UPDATE knowledge_items 
SET content = '기초모델링은 3D 모델링의 기본이 되는 기술입니다. 여기에는 버텍스, 엣지, 페이스와 같은 기본 요소의 이해와 조작이 포함됩니다. 또한 모델링 소프트웨어의 기본 도구 사용법과 워크플로우도 다룹니다.'
WHERE id = 11;

-- 폴리곤 모델링 상세 내용
UPDATE knowledge_items 
SET content = '폴리곤 모델링은 가장 일반적인 3D 모델링 방식입니다. 정점(vertex), 모서리(edge), 면(face)을 사용하여 3D 오브젝트를 만듭니다. 게임 캐릭터, 건축물, 일상 용품 등 대부분의 3D 모델이 이 방식으로 제작됩니다.'
WHERE id = 111;

-- 프로시저럴 모델링 상세 내용
UPDATE knowledge_items 
SET content = '프로시저럴 모델링은 규칙과 알고리즘을 기반으로 3D 모델을 자동으로 생성하는 기법입니다. 도시, 지형, 식물 등 복잡하고 반복적인 패턴을 가진 모델을 효율적으로 생성할 수 있습니다.'
WHERE id = 12;

-- 프로그래밍 관련 상세 내용
UPDATE knowledge_items 
SET content = '프로그래밍은 컴퓨터에게 특정 작업을 수행하도록 지시하는 과정입니다. 여기에는 웹 개발, 앱 개발, 게임 개발, 데이터 분석 등 다양한 분야가 포함됩니다.'
WHERE id = 2;

-- 웹코딩 상세 내용
UPDATE knowledge_items 
SET content = '웹코딩은 웹사이트와 웹 애플리케이션을 만드는 기술입니다. HTML, CSS, JavaScript를 기본으로 하며, 다양한 프레임워크와 라이브러리를 활용하여 현대적인 웹 서비스를 구축합니다.'
WHERE id = 21;

-- Frontend 개발 상세 내용
UPDATE knowledge_items 
SET content = 'Frontend 개발은 사용자가 직접 보고 상호작용하는 웹사이트의 부분을 만드는 것입니다. HTML로 구조를 잡고, CSS로 스타일을 입히며, JavaScript로 동적 기능을 구현합니다. React, Vue, Angular 등의 프레임워크도 많이 사용됩니다.'
WHERE id = 211;

-- Backend 개발 상세 내용
UPDATE knowledge_items 
SET content = 'Backend 개발은 서버 측 로직을 구현하는 것입니다. 데이터베이스 관리, API 개발, 서버 보안, 성능 최적화 등을 담당합니다. Python, Node.js, Java 등 다양한 언어와 프레임워크가 사용됩니다.'
WHERE id = 212;

-- 피지컬 컴퓨팅 상세 내용
UPDATE knowledge_items 
SET content = '피지컬 컴퓨팅은 디지털 기술과 물리적 세계를 연결하는 분야입니다. 센서로 물리적 데이터를 수집하고, 액추에이터로 물리적 반응을 만들어내는 등 하드웨어와 소프트웨어를 통합적으로 다룹니다.'
WHERE id = 22;

-- 아두이노 상세 내용
UPDATE knowledge_items 
SET content = '아두이노는 오픈소스 하드웨어 플랫폼입니다. 간단한 마이크로컨트롤러 보드와 개발 환경을 제공하여, LED 제어부터 로봇 제작까지 다양한 전자 프로젝트를 구현할 수 있습니다.'
WHERE id = 221;

-- 알고리즘 상세 내용
UPDATE knowledge_items 
SET content = '알고리즘은 문제 해결을 위한 단계적인 절차입니다. 정렬, 검색, 그래프 탐색 등의 기본 알고리즘부터 머신러닝에 사용되는 복잡한 알고리즘까지 다양한 종류가 있습니다.'
WHERE id = 23;

-- 데이터베이스 상세 내용
UPDATE knowledge_items 
SET content = '데이터베이스는 구조화된 데이터를 효율적으로 저장하고 관리하는 시스템입니다. SQL, NoSQL 등 다양한 유형이 있으며, 데이터 모델링, 쿼리 최적화, 트랜잭션 관리 등의 개념을 다룹니다.'
WHERE id = 24;
