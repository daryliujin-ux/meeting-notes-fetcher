#!/usr/bin/env python3
"""
智能会议纪要筛选系统 - 简化版
专注: 半导体 / 互联网 / 新能源 / 高端制造
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SmartFilter:
    """智能筛选器"""
    
    def __init__(self):
        # 行业关键词配置
        self.industry_keywords = {
            # 半导体
            '半导体': ['半导体', '芯片', '集成电路', '国产替代', '晶圆', '封测'],
            
            # 互联网
            '互联网': ['互联网', 'AI', '人工智能', '云计算', '大数据', '软件', 'SaaS', '电商'],
            
            # 新能源
            '新能源': ['新能源', '光伏', '风电', '储能', '锂电池', '新能源车', '充电桩', '电池'],
            
            # 高端制造
            '高端制造': ['高端制造', '智能制造', '工业自动化', '机器人', '数控', '工业母机']
        }
        
        # 高优先级关键词
        self.high_priority = ['策略', '宏观', '半导体', 'AI', '人工智能']
        
        # 中优先级关键词
        self.medium_priority = ['新能源', '光伏', '储能', '互联网', '高端制造', '智能制造']
    
    def match(self, title: str, category: str) -> Tuple[bool, str, Optional[str]]:
        """
        匹配会议
        返回: (是否匹配, 匹配原因, 优先级)
        """
        text = f"{title} {category}"
        
        # 检查高优先级
        for keyword in self.high_priority:
            if keyword in text:
                return (True, f"高优先级: {keyword}", "HIGH")
        
        # 检查行业匹配
        for industry, keywords in self.industry_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    priority = "MEDIUM" if industry in ['新能源', '互联网', '高端制造'] else "HIGH"
                    return (True, f"{industry}: {keyword}", priority)
        
        # 检查中优先级
        for keyword in self.medium_priority:
            if keyword in text:
                return (True, f"关键词: {keyword}", "MEDIUM")
        
        return (False, "不匹配", None)


class MeetingFetcher:
    """会议抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.filter = SmartFilter()
    
    def fetch_meetings(self) -> List[Dict]:
        """获取会议列表"""
        # 示例数据
        meetings = [
            {
                "id": "2084617",
                "title": "中信证券策略聚焦专题会：缩圈，聚焦",
                "date": "2026-04-06",
                "time": "19:30",
                "category": "策略",
                "url": "https://research.citics.com/tel/info/1_2084617"
            },
            {
                "id": "2084644",
                "title": "电子观点每周谈第91期：电子行业亮马组合",
                "date": "2026-04-06",
                "time": "19:00",
                "category": "电子",
                "url": "https://research.citics.com/tel/info/1_2084644"
            },
            {
                "id": "2084623",
                "title": "光通信和国产算力推荐",
                "date": "2026-04-06",
                "time": "19:30",
                "category": "通信",
                "url": "https://research.citics.com/tel/info/1_2084623"
            },
            {
                "id": "2083392",
                "title": "电池与能源管理行业周度观察",
                "date": "2026-04-06",
                "time": "19:30",
                "category": "新能源",
                "url": "https://research.citics.com/tel/info/1_2083392"
            },
            {
                "id": "2084609",
                "title": "输入型通胀的中国路径",
                "date": "2026-04-06",
                "time": "19:00",
                "category": "宏观",
                "url": "https://research.citics.com/tel/info/1_2084609"
            },
            {
                "id": "2083404",
                "title": "科技产业周周谈：AI算力需求分析",
                "date": "2026-04-06",
                "time": "20:00",
                "category": "科技",
                "url": "https://research.citics.com/tel/info/1_2083404"
            }
        ]
        
        logger.info(f"获取到 {len(meetings)} 个会议")
        return meetings
    
    def filter_meetings(self, meetings: List[Dict]) -> Dict:
        """筛选会议"""
        matched = []
        
        for meeting in meetings:
            is_match, reason, priority = self.filter.match(
                meeting['title'], 
                meeting['category']
            )
            
            if is_match:
                meeting_info = {
                    **meeting,
                    'match_reason': reason,
                    'priority': priority
                }
                matched.append(meeting_info)
                logger.info(f"✅ {meeting['title'][:30]} - {reason}")
            else:
                logger.info(f"❌ {meeting['title'][:30]} - {reason}")
        
        # 排序
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        matched.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return {
            'matched': matched,
            'excluded': [m for m in meetings if m not in [mm for mm in matched]]
        }
    
    def generate_report(self, result: Dict) -> str:
        """生成报告"""
        lines = []
        lines.append("# 📊 会议纪要筛选报告")
        lines.append(f"\n**筛选时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n**筛选条件**: 半导体 / 互联网 / 新能源 / 高端制造")
        lines.append(f"\n| 项目 | 数量 |")
        lines.append(f"|------|------|")
        lines.append(f"| 匹配会议 | {len(result['matched'])} |")
        
        if result['matched']:
            lines.append("\n---\n")
            lines.append("## ✅ 匹配的会议\n")
            
            for i, m in enumerate(result['matched'], 1):
                emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(m['priority'], "⚪")
                lines.append(f"### {i}. {m['title']} {emoji}")
                lines.append(f"- **时间**: {m['date']} {m['time']}")
                lines.append(f"- **匹配**: {m['match_reason']}")
                lines.append(f"- **链接**: [{m['url']}]({m['url']})")
                lines.append("")
        
        return "\n".join(lines)
    
    def save_notes(self, matched: List[Dict]):
        """保存纪要"""
        output_dir = "output/matched_notes"
        os.makedirs(output_dir, exist_ok=True)
        
        for m in matched:
            filename = f"{m['date']}_{m['id']}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {m['title']}\n\n")
                f.write(f"**时间**: {m['date']} {m['time']}\n")
                f.write(f"**匹配**: {m['match_reason']}\n")
                f.write(f"**优先级**: {m['priority']}\n")
                f.write(f"**链接**: {m['url']}\n")
            
            logger.info(f"保存: {filepath}")


def main():
    """主函数"""
    logger.info("="*60)
    logger.info("智能筛选系统启动")
    logger.info("关注: 半导体 / 互联网 / 新能源 / 高端制造")
    logger.info("="*60)
    
    fetcher = MeetingFetcher()
    
    # 1. 获取会议
    meetings = fetcher.fetch_meetings()
    
    # 2. 筛选
    result = fetcher.filter_meetings(meetings)
    
    # 3. 生成报告
    report = fetcher.generate_report(result)
    
    print("\n" + report)
    
    # 4. 保存
    os.makedirs("output", exist_ok=True)
    with open("output/filter_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    if result['matched']:
        fetcher.save_notes(result['matched'])
    
    # 5. 推送通知
    high_priority = [m for m in result['matched'] if m['priority'] == 'HIGH']
    if high_priority:
        print(f"\n🔔 高优先级会议 {len(high_priority)} 个:")
        for m in high_priority:
            print(f"   🔴 {m['title']}")
    
    logger.info("="*60)
    logger.info("完成")
    logger.info("="*60)


if __name__ == "__main__":
    main()
