1. 이미지 캡처 및 업로드
로봇이 이미지 캡처

로봇이 작물의 이미지를 촬영하여 클라우드에 전송할 준비를 합니다.
AWS 스토리지(S3)에 업로드

AWS 서비스: Amazon S3
설명: 촬영된 이미지는 Amazon S3 버킷에 업로드됩니다. S3는 안전하고 확장 가능한 스토리지를 제공하며, 원본 이미지의 초기 저장 위치로 사용됩니다.
구현 팁: 보안을 위해 로봇의 IAM 역할만 업로드 권한을 가지도록 S3 버킷 권한을 설정합니다.

2. 이미지 처리 및 분석
API 호출을 위한 트리거 생성

AWS 서비스: Amazon S3 이벤트 알림
설명: S3 이벤트 알림을 통해 새로운 이미지 업로드가 감지되면 분석 워크플로우가 자동으로 시작됩니다. 이 이벤트는 이미지를 처리하기 위해 Lambda 함수 또는 API Gateway를 트리거합니다.
이미지를 API에 전송하여 분석

AWS 서비스: AWS Lambda 및 API Gateway
설명: Lambda 함수가 S3에서 이미지를 가져와 사전에 정의된 API 엔드포인트에 전송하여 분석을 진행합니다. API는 이미지를 처리하고, 병충해나 작물 건강 정보를 포함한 JSON 형식의 결과를 반환합니다.
구현 팁: API Gateway를 사용하여 Lambda 함수가 외부 API에 안전하게 접근하도록 설정합니다.

3. JSON 파일 저장 및 데이터베이스 업데이트
분석 결과 JSON 파일 저장
AWS 서비스: Amazon DynamoDB
설명: API로부터 받은 JSON 파일은 DynamoDB에 저장됩니다. 이 데이터베이스는 구조화된 데이터를 신속하게 관리할 수 있어 후속 처리에 적합합니다.
구현 팁: 분석 결과가 저장될 DynamoDB 테이블의 스키마를 설계하고, 필요한 인덱스를 설정해 효율적인 검색이 가능하도록 합니다.

4. 데이터 프론트엔드 전달
프론트엔드에서 데이터 호출
AWS 서비스: Amazon API Gateway
설명: 프론트엔드는 API Gateway를 통해 DynamoDB에 저장된 분석 결과 JSON 데이터를 호출합니다. 이를 통해 사용자는 실시간으로 작물 상태와 병충해 진단 결과를 확인할 수 있습니다.
구현 팁: 데이터 전달의 보안을 위해 API Gateway에 인증 및 권한을 설정하여 필요한 사용자만 접근할 수 있도록 합니다.