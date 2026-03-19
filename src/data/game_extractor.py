from typing import List, Dict, Optional
from src.browser.page_handler import PageHandler
from src.utils.logger import get_logger


class GameExtractor:
    def __init__(self, page_handler: PageHandler):
        self.page_handler = page_handler
        self.logger = get_logger()
    
    def extract_games_from_table(self) -> List[Dict[str, str]]:
        try:
            self.logger.info("开始提取赛事信息...")
            
            games = []
            
            tables = self.page_handler.page.query_selector_all('table')
            self.logger.info(f"找到 {len(tables)} 个表格")
            
            if len(tables) < 2:
                self.logger.warning("页面表格数量不足，无法提取赛事信息")
                return []
            
            target_table = tables[1]
            rows = target_table.query_selector_all('tr')
            self.logger.info(f"目标表格中有 {len(rows)} 行")
            
            for row in rows:
                cells = row.query_selector_all('td')
                if len(cells) >= 11:
                    game_info = {}
                    
                    for i, cell in enumerate(cells):
                        text = cell.text_content().strip()
                        
                        if i == 0:
                            game_info['序号'] = text
                        elif i == 1:
                            game_info['比赛ID'] = text
                        elif i == 2:
                            game_info['比赛名称'] = text
                        elif i == 3:
                            game_info['比赛描述'] = text
                        elif i == 4:
                            game_info['团队名称'] = text
                        elif i == 5:
                            game_info['创建日期'] = text
                        elif i == 6:
                            game_info['所属赛区'] = text
                        elif i == 7:
                            game_info['创建人'] = text
                        elif i == 8:
                            game_info['比赛状态'] = text
                        elif i == 9:
                            game_info['报名情况'] = text
                        elif i == 10:
                            game_info['操作'] = text
                            
                            # 提取链接
                            link = cell.query_selector('a[href]')
                            if link:
                                href = link.get_attribute('href')
                                if href:
                                    game_info['url'] = href
                    
                    if game_info and '比赛名称' in game_info:
                        games.append(game_info)
                        self.logger.debug(f"提取到赛事: {game_info.get('比赛名称', 'Unknown')}")
            
            self.logger.info(f"总共提取到 {len(games)} 个赛事")
            return games
            
        except Exception as e:
            self.logger.error(f"提取赛事信息失败: {e}")
            return []
    
    def extract_games_with_links(self) -> List[Dict[str, str]]:
        try:
            self.logger.info("开始提取带链接的赛事信息...")
            
            games = []
            
            links = self.page_handler.page.query_selector_all('a[href]')
            self.logger.info(f"找到 {len(links)} 个链接")
            
            for link in links:
                href = link.get_attribute('href')
                text = link.text_content().strip()
                
                if href and text and 'game' in href.lower():
                    game_info = {
                        'name': text,
                        'url': href
                    }
                    games.append(game_info)
                    self.logger.debug(f"提取到赛事链接: {text} -> {href}")
            
            self.logger.info(f"总共提取到 {len(games)} 个赛事链接")
            return games
            
        except Exception as e:
            self.logger.error(f"提取赛事链接失败: {e}")
            return []
    
    def get_game_details(self, game_url: str) -> Optional[Dict[str, str]]:
        try:
            self.logger.info(f"获取赛事详情: {game_url}")
            
            if not self.page_handler.navigate(game_url):
                self.logger.error("无法导航到赛事页面")
                return None
            
            details = {}
            
            # 提取赛事名称
            title_elem = self.page_handler.page.query_selector('h1, h2, .title, .game-name')
            if title_elem:
                details['title'] = title_elem.text_content().strip()
            
            # 提取其他信息
            info_elements = self.page_handler.page.query_selector_all('.info, .detail, .description')
            for elem in info_elements:
                text = elem.text_content().strip()
                if text and len(text) > 10:
                    details['description'] = text
                    break
            
            self.logger.info(f"获取到赛事详情: {details.get('title', 'Unknown')}")
            return details
            
        except Exception as e:
            self.logger.error(f"获取赛事详情失败: {e}")
            return None