import React, { useState, useRef, useEffect } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import SpriteText from 'three-spritetext';
import KnowledgePopup from './KnowledgePopup';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const createLinks = (nodes) => {
  const links = [];
  const nodeMap = new Map(nodes.map(node => [node.id, node]));

  nodes.forEach(node1 => {
    nodes.forEach(node2 => {
      // 같은 노드가 아닌 경우만 처리
      if (node1.id !== node2.id) {
        // 공통 태그 찾기
        const commonTags = node1.tags.filter(tag => node2.tags.includes(tag));
        
        // 태그가 하나라도 공통인 경우에만 연결 고려
        if (commonTags.length > 0) {
          const levelDiff = Math.abs(node1.level - node2.level);
          
          // 규칙 1: 한 단계 레벨 차이가 나는 노드 연결
          if (levelDiff === 1) {
            links.push({
              source: node1.id,
              target: node2.id,
              commonTags
            });
          }
          // 규칙 2: 같은 레벨의 노드 연결 (부모 노드 확인)
          else if (levelDiff === 0) {
            // 각 노드의 부모 노드 찾기 (한 단계 높은 레벨의 연결된 노드)
            const node1Parents = findParentNodes(node1, links, nodeMap);
            const node2Parents = findParentNodes(node2, links, nodeMap);
            
            // 부모 노드를 공유하지 않는 경우에만 연결
            const hasCommonParent = node1Parents.some(parent1 => 
              node2Parents.some(parent2 => parent1 === parent2)
            );
            
            if (!hasCommonParent) {
              links.push({
                source: node1.id,
                target: node2.id,
                commonTags
              });
            }
          }
        }
      }
    });
  });
  
  console.log('Created links:', links);
  return links;
};

// 노드의 부모 노드들을 찾는 함수
const findParentNodes = (node, links, nodeMap) => {
  return links
    .filter(link => 
      (link.source === node.id || link.target === node.id) &&
      (nodeMap.get(link.source).level === node.level + 1 || 
       nodeMap.get(link.target).level === node.level + 1)
    )
    .map(link => {
      const otherId = link.source === node.id ? link.target : link.source;
      return nodeMap.get(otherId).id;
    });
};

const Graph = () => {
  const fgRef = useRef();
  const containerRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const [hoverNode, setHoverNode] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  // Fetch data from database
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}/knowledge/files`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const knowledgeItems = data.files || [];
        
        // Process nodes
        const nodes = knowledgeItems.map(item => ({
          id: item.id || item.filename,
          name: item.title,
          level: Math.min(item.level, 4),
          tags: Array.isArray(item.tags) ? item.tags : [],
          group: item.level,
          content: item.content,
          summary: item.summary,
          references: Array.isArray(item.references) ? item.references : []
        }));

        // Create links based on the nodes
        const links = createLinks(nodes);
        setGraphData({ nodes, links });

        // Add neighbors and links information
        links.forEach(link => {
          const a = nodes.find(node => node.id === link.source);
          const b = nodes.find(node => node.id === link.target);
          !a.neighbors && (a.neighbors = []);
          !b.neighbors && (b.neighbors = []);
          a.neighbors.push(b);
          b.neighbors.push(a);
          !a.links && (a.links = []);
          !b.links && (b.links = []);
          a.links.push(link);
          b.links.push(link);
        });
      } catch (error) {
        console.error('Error fetching knowledge data:', error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const handleResize = () => {
      if (containerRef.current) {
        const { width, height } = document.body.getBoundingClientRect();
        const size = Math.min(width, height) * 0.6; 
        setDimensions({
          width: size,
          height: size
        });
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.cameraPosition({ x: 0, y: 0, z: 400 });
      fgRef.current.d3Force('link').distance(50);
      fgRef.current.d3Force('charge').strength(-100);
    }
  }, []);

  const handleNodeClick = node => {
    setSelectedNode(node);
  };

  const handleNodeHover = node => {
    highlightNodes.clear();
    highlightLinks.clear();
    if (node) {
      highlightNodes.add(node);
      node.neighbors?.forEach(neighbor => highlightNodes.add(neighbor));
      node.links?.forEach(link => highlightLinks.add(link));
    }
    setHoverNode(node || null);
    setHighlightNodes(new Set(highlightNodes));
    setHighlightLinks(new Set(highlightLinks));
  };

  const getNodeColor = node => {
    if (highlightNodes.has(node)) {
      return node === hoverNode ? '#ff0000' : '#ff6b6b';
    }
    
    if (node.tags.includes('3D')) {
      return '#4CAF50';
    } else if (node.tags.includes('ai')) {
      return '#2196F3';
    } else if (node.tags.includes('dev')) {
      return '#FFC107';
    }
    return '#ffffff';
  };

  const getNodeSize = level => {
    switch(level) {
      case 1: return 12;
      case 2: return 8;
      case 3: return 6;
      case 4: return 6;
      default: return 6;
    }
  };

  const getNodeWeight = level => {
    switch(level) {
      case 1: return 'bold';
      case 2: return '600';
      case 3: return '600';
      case 4: return 'normal';
      default: return 'normal';
    }
  };

  return (
    <>
      <div className="fixed inset-0 flex items-center justify-center" style={{ backgroundColor: '#dddddd' }}>
        {/* 프로필 정보 - 상단 좌측 */}
        <div className="absolute top-16 left-16 text-gray-800">
          <div className="flex items-center gap-6">
            <h1 className="text-3xl font-bold">이승훈</h1>
            <h2 className="text-xl">3D Artist & Developer</h2>
            <span className="text-gray-400 mx-2">|</span>
            <a 
              href="https://instagram.com/aengmung3d" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              @aengmung3d
            </a>
            <span className="text-gray-400">|</span>
            <a 
              href="https://instagram.com/dodand3d" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              @dodand3d
            </a>
          </div>
        </div>

        {/* 컨텐츠 컨테이너 */}
        <div className="flex items-center justify-center" style={{ width: '100%', padding: '0 8rem' }}>
          {/* 그래프 캔버스 */}
          <motion.div 
            ref={containerRef}
            initial={false}
            animate={{ 
              x: selectedNode ? '-70%' : '0%'
            }}
            transition={{ 
              type: "spring",
              stiffness: 150,
              damping: 25,
              mass: 1
            }}
            style={{ 
              width: dimensions.width,
              height: dimensions.height,
              borderRadius: '30%',
              overflow: 'hidden',
              backgroundColor: '#000003',
              boxShadow: '0 0 50px rgba(0, 0, 0, 0.5)',
              position: 'relative'
            }}
          >
            <ForceGraph3D
              ref={fgRef}
              width={dimensions.width}
              height={dimensions.height}
              graphData={graphData}
              backgroundColor="#000003"
              nodeThreeObject={node => {
                const sprite = new SpriteText(node.name);
                sprite.color = getNodeColor(node);
                sprite.textHeight = getNodeSize(node.level);
                sprite.fontWeight = getNodeWeight(node.level);
                sprite.userData = { ...node };
                return sprite;
              }}
              linkDirectionalParticles={0}
              linkColor={link => highlightLinks.has(link) ? '#ff0000' : '#ffffff'}
              linkOpacity={0.5}
              linkWidth={0.7}
              onNodeHover={handleNodeHover}
              onNodeClick={handleNodeClick}
              nodeThreeObjectExtend={false}
              controlType="orbit"
              d3VelocityDecay={0.3}
              nodeRelSize={6}
              showNavInfo={false}
            />
          </motion.div>
        </div>
      </div>
      <KnowledgePopup 
        node={selectedNode} 
        onClose={() => setSelectedNode(null)}
        isVisible={!!selectedNode}
        dimensions={dimensions}
      />
    </>
  );
};

export default Graph;
