// 노드 레벨에 따른 색상 반환
export const getNodeColor = (level) => {
  switch (level) {
    case 1:
      return '#4CAF50';  // 초록색
    case 2:
      return '#2196F3';  // 파란색
    case 3:
      return '#FFC107';  // 노란색
    case 4:
      return '#9C27B0';  // 보라색
    case 5:
      return '#F44336';  // 빨간색
    default:
      return '#FFFFFF';  // 흰색
  }
};
