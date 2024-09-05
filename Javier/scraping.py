# Import the requests library to make HTTP requests
import requests
# Import the BeautifulSoup class from the bs4 module for parsing HTML
from bs4 import BeautifulSoup
import urllib3
import time

# Import the necessary classes and modules from the Selenium library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Define the URL of the web page to scrape
url = 'https://inside.fifa.com/fifa-world-ranking/men'


# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
driver.get(url)
WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    ).click()
#time.sleep(10)
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"table")))
time.sleep(20)
soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(5)
driver.quit()
#print(soup)

#table_rows = soup.find_all('tr', {'class': 'table-row-module_row__3wRGf table-row-module_hover__MdRZU table-row-module_regular__tAYiC data-grid-module_pointer__uipYu base-world-ranking-table_tableRow__fC_zY'})
#rows = table.find('tbody').find_all('tr')
#print(rows)
print('W'*10)
td = soup.find_all('td')
print(td)



# for row in table_rows:
#     # Extract rank
#     rank = row.find('span', {'class': 'rank-cell_rank__yNDOI'}).text if row.find('span', {'class': 'rank-cell_rank__yNDOI'}) else 'N/A'
    
#     # Extract team name
#     team_name = row.find('a', {'class': 'team-cell_teamName__tyiAD'}).text if row.find('a', {'class': 'team-cell_teamName__tyiAD'}) else 'N/A'
    
#     # Extract team code
#     team_code = row.find('a', {'class': 'team-cell_teamCode__Yi4NC'}).text if row.find('a', {'class': 'team-cell_teamCode__Yi4NC'}) else 'N/A'
    
#     # Extract total points
#     total_points = row.find('span', {'class': 'total-points-cell_points__JPjv3'}).text if row.find('span', {'class': 'total-points-cell_points__JPjv3'}) else 'N/A'
    
#     print(f"Rank: {rank}, Team: {team_name}, Code: {team_code}, Points: {total_points}")

## table-row-module_row__3wRGf table-row-module_hover__MdRZU table-row-module_regular__tAYiC data-grid-module_pointer__uipYu base-world-ranking-table_tableRow__fC_zY
## .table-row-module_row__3wRGf:nth-child(1) .rank-cell_rank__yNDOI
# <table class="table-module_table__76hUL fcds-table" role="table">

# <tr role="row" class="table-row-module_row__3wRGf table-row-module_hover__MdRZU table-row-module_regular__tAYiC data-grid-module_pointer__uipYu base-world-ranking-table_tableRow__fC_zY"><td class="table-cell-module_cell__tAaKX cell" role="cell" style="width: 120px;"><div class="rank-cell_wrapper__Qx1NH" aria-label="1"><span class="rank-cell_rank__yNDOI">1</span><div class="rank-cell_positionNoChangeWrapper__gwYit"><span class="rank-cell_dot___S2Mb"></span></div></div></td><td class="table-cell-module_cell__tAaKX cell" role="cell" style="width: auto;"><div class="team-cell_teamCell__lZR3O"><div class="country-flag_flagWrapper__arhxZ"><div class="image-module_fcdsImageContainer__xKYYN image-module_withoutAspectRatio__JxxpR  "><picture class="image-module_picture__IXVaz "><source media="(min-width: 1440px)" srcset="https://api.fifa.com/api/v3/picture/flags-sq-2/ARG"><source media="(min-width: 1280px)" srcset="https://api.fifa.com/api/v3/picture/flags-sq-2/ARG"><source media="(min-width: 1024px)" srcset="https://api.fifa.com/api/v3/picture/flags-sq-2/ARG"><source media="(min-width: 720px)" srcset="https://api.fifa.com/api/v3/picture/flags-sq-2/ARG"><source media="(max-width:  720px)" srcset="https://api.fifa.com/api/v3/picture/flags-sq-2/ARG"><img class="image-module_horizontalImage__c5hRK" decoding="async" loading="lazy" src="https://api.fifa.com/api/v3/picture/flags-sq-2/ARG" alt="Argentina" title="Argentina" width="100%" height="100%" style="--object-fit-strategy: cover;"></picture></div></div><a class="link-module_link__F9IVG team-cell_teamName__tyiAD" href="/fifa-world-ranking/ARG?gender=men">Argentina</a><a class="link-module_link__F9IVG team-cell_teamCode__Yi4NC" href="/fifa-world-ranking/ARG?gender=men">ARG</a></div></td><td class="table-cell-module_cell__tAaKX cell" role="cell" style="width: 150px;"><span class="total-points-cell_points__JPjv3">1901.48</span></td>
# <td class="table-cell-module_cell__tAaKX cell" role="cell" style="width: 150px;"><span class="previous-points-cell_points__rerY5">1860.14</span></td><td class="table-cell-module_cell__tAaKX cell" role="cell" style="width: 150px;"><span class="points-difference-cell_points__0dCZw">+41.34</span></td><td class="table-cell-module_cell__tAaKX cell" role="cell" style="width: 250px;"><div class="matches-window-cell_matchWindowContainer__Yxn80"><div data-tooltip-id="454.67213277924134" class="matches-window-cell_singleMatchCircle__CJxeV" style="background: var(--fcds-green);">W</div><div class="tooltip-module_tooltipWrapper__XRg0Q"></div><div data-tooltip-id="984.5748709210886" class="matches-window-cell_singleMatchCircle__CJxeV" style="background: var(--fcds-green);">W</div><div class="tooltip-module_tooltipWrapper__XRg0Q"></div><div data-tooltip-id="69.44985393658176" class="matches-window-cell_singleMatchCircle__CJxeV" style="background: var(--fcds-green);">W</div><div class="tooltip-module_tooltipWrapper__XRg0Q"><div id="69.44985393658176" role="tooltip" class="react-tooltip core-styles-module_tooltip__3vRRp styles-module_tooltip__mnnfp styles-module_dark__xNqje tooltip-module_tooltip__e-rkz react-tooltip__place-top core-styles-module_closing__sGnxF react-tooltip__closing" style="padding: 0px; z-index: 999; left: 602.969px; top: 443.579px;"><div class="d-flex flex-column match-card-module_card__yUEVd matches-window-cell_matchCardTooltip__ceQr9"><div class="match-card-module_header__7G-oZ match-card-module_fontSize10__85E4p">Copa America 2024</div><div class="match-card-module_cardContainer__KufUI"><div class="d-flex flex-column match-card-module_cardContent__ylKW8"><div class="d-flex justify-content-between align-items-center match-card-module_fontSize10__85E4p"><b>Quarter-final</b><div class="d-flex align-items-center"><div class="d-flex align-items-center"><p>04 July 2024</p></div></div></div><div class=""><div class="match-card-module_teams__GI4jz"><div class="d-flex align-items-center justify-content-between match-card-module_height24__1g9ob"><div class="d-flex align-items-center"><div class="match-card-module_logo__5k4gZ match-card-module_flags__Hd7qk d-flex justify-content-center team-logo-module_withBorder__nSpJm"><img src="https://api.fifa.com/api/v3/picture/flags-sq-4/ARG" alt="Home team logo" loading="lazy" class="d-block"></div><div class="ml-8 match-card-module_fontSize12__bQoS9"><span>Argentina</span><p class="match-card-module_winPenaltyCaption__twQrf match-card-module_fontSize10__85E4p">Won 4 - 2 On Penalties</p></div></div><div class="d-flex align-items-center match-card-module_fontSize12__bQoS9"><div class="match-card-module_score__QLj83 d-flex align-items-center justify-content-center"><b>1</b></div><b class="mx-4 match-card-module_penScore__6zsWP">(4)</b></div></div><div class="d-flex justify-content-between align-items-center match-card-module_height24__1g9ob"><div class="d-flex align-items-center"><div class="match-card-module_logo__5k4gZ match-card-module_flags__Hd7qk d-flex justify-content-center team-logo-module_withBorder__nSpJm"><img src="https://api.fifa.com/api/v3/picture/flags-sq-4/ECU" alt="Away team logo" loading="lazy" class="d-block"></div><div class="ml-8 match-card-module_fontSize12__bQoS9"><span>Ecuador</span></div></div><div class="match-card-module_fontSize12__bQoS9 d-flex align-items-center"><div class="match-card-module_score__QLj83 d-flex align-items-center justify-content-center"><b>1</b></div><b class="mx-4 match-card-module_penScore__6zsWP">(2)</b></div></div></div><div class="d-none align-items-center"><div class="d-flex align-items-center"><p>04 July 2024</p></div></div></div></div></div></div><div class="react-tooltip-arrow core-styles-module_arrow__cvMwQ styles-module_arrow__K0L3T" style="left: 116px; bottom: -4px;"></div></div></div><div data-tooltip-id="633.3728208821869" class="matches-window-cell_singleMatchCircle__CJxeV" style="background: var(--fcds-green);">W</div><div class="tooltip-module_tooltipWrapper__XRg0Q"></div><div data-tooltip-id="782.2296003062412" class="matches-window-cell_singleMatchCircle__CJxeV" style="background: var(--fcds-green);">W</div><div class="tooltip-module_tooltipWrapper__XRg0Q"></div><div data-tooltip-id="687.3879160777454" class="matches-window-cell_singleMatchCircle__CJxeV" style="background: var(--fcds-green);">W</div><div class="tooltip-module_tooltipWrapper__XRg0Q"></div><div data-tooltip-id="62.82311290404419" class="matches-window-cell_singleMatchCircle__CJxeV" style="background: var(--fcds-green);">W</div><div class="tooltip-module_tooltipWrapper__XRg0Q"></div></div></td><td class="table-cell-module_cell__tAaKX table-cell-module_cellRight__3-nFC cell" role="cell" align="right" width="20px"><button class="icon-button-module_buttonTheme__eLhpm icon-button-module_tertiaryVariant__nzxT7 icon-button-module_darkenOnHover__HbNIb icon-button-module_iconButton__3SlSv table-row-module_expandIconButton__cIZIP" style="--icon-size: 1.5rem;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.9933 15.9973L10.5932 14.5973L10.6003 14.5902L5.70011 9.68997C5.31351 9.30336 5.31351 8.67656 5.70011 8.28995C6.08671 7.90335 6.71352 7.90335 7.10012 8.28995L12.0003 13.1902L16.9003 8.29021C17.2869 7.9036 17.9138 7.9036 18.3004 8.29021C18.687 8.67683 18.687 9.30365 18.3004 9.69027L13.4004 14.5902L13.4073 14.5971L12.0073 15.9972C12.0035 15.9933 11.9971 15.9935 11.9933 15.9973Z" fill="currentColor"></path></svg></button></td></tr>