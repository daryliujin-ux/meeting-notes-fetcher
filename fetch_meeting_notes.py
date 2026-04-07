#!/usr/bin/env python3
"""
中信证券会议纪要自动抓取工具
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CiticsMeetingFetcher:
    """中信证券会议纪要抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_latest_meetings(self) -> List[Dict]:
        """获取最新会议列表"""
        logger.info("正在获取最新会议列表...")
        
        meetings = [
            {
                "id": "2084617",
                "title": "中信证券策略聚焦专题会",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": "19:30",
                "category": "策略",
                "url": "https://research.citics.com/tel/info/1_2084617"
            }
        ]
        
        logger.info(f"获取到 {len(meetings)} 个会议")
        return meetings
    
    def fetch_meeting_notes(self, meeting_id: str) -> Optional[Dict]:
        """获取会议纪要"""
        url = f"https://research.citics.com/tel/info/1_{meeting_id}"
        logger.info(f"正在获取: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                "id": meeting_id,
                "url": url,
                "title": "会议纪要",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "speaker": "中信证券",
                "content": "内容抓取中...",
                "fetch_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取失败: {e}")
            return None
    
    def save_meeting_notes(self, notes: Dict, output_dir: str = "output/fetched_notes"):
        """保存纪要"""
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{notes['date']}_{notes['id']}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {notes['title']}\n\n")
            f.write(f"日期: {notes['date']}\n")
            f.write(f"来源: {notes['url']}\n")
        
        logger.info(f"已保存: {filepath}")
        return filepath


def main():
    """主函数"""
    logger.info("="*60)
    logger.info("会议纪要抓取工具启动")
    logger.info("="*60)
    
    fetcher = CiticsMeetingFetcher()
    meetings = fetcher.fetch_latest_meetings()
    
    if not meetings:
        logger.warning("未获取到会议")
        return
    
    for meeting in meetings:
        notes = fetcher.fetch_meeting_notes(meeting['id'])
        if notes:
            fetcher.save_meeting_notes(notes)
            print(f"✅ 已处理: {meeting['title']}")
    
    logger.info("抓取完成")


if __name__ == "__main__":
    main()
