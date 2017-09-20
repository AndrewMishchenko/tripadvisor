import multiprocessing
import os
import re
import time

import xlwt
from selenium import webdriver

# firefox_profile = webdriver.FirefoxProfile()
# firefox_profile.set_preference('permissions.default.stylesheet', 2)
# firefox_profile.set_preference('permissions.default.image', 2)
# firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')



d_path = os.getcwd() + '/geckodriver'

domain = 'https://www.tripadvisor.co.uk/Restaurants-g186338-c8-London_England.html#EATERY_OVERVIEW_BOX'


def get_links():
    driver = webdriver.Firefox(executable_path=d_path)
    driver.get(domain)
    time.sleep(2)
    n_p = True
    while n_p:
        try:
            for href in driver.find_elements_by_css_selector('a.property_title'):
                with open('hrefs.txt', 'a') as doc:
                    doc.write(href.get_attribute('href') + '\n')
            next_page = driver.find_element_by_css_selector('a.next')
            next_page.click()
            time.sleep(2)

        except Exception as err:
            print(err)
            n_p = False
            driver.close()
            return


def get_saved_links():  # gets all saved links
    with open('hrefs.txt', 'r') as doc:
        return [href.replace('\n', '') for href in doc]


def get_mail(driver):
    cont_hrefs = []
    for href in driver.find_elements_by_css_selector('a'):
        try:
            href = href.get_attribute('href')
            if 'contact' in href:
                cont_hrefs.append(href)
        except Exception:
            continue

    # check mails on the main page
    page = driver.page_source
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', page)
    for href in set(cont_hrefs):
        driver.get(href)
        time.sleep(5)
        page = driver.page_source
        emails += re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', page)
    return emails


def get_page_content(url):
    try:
        driver = webdriver.Firefox(executable_path=d_path)
        driver.get(url)
        time.sleep(2)
        try:
            name_of_cafe = driver.find_element_by_css_selector('h1.heading_title').text
        except Exception:
            name_of_cafe = ''

        try:
            address = driver.find_element_by_css_selector('.address').text.replace('|', '-')
        except Exception:
            address = ''

        try:
            phone = driver.find_element_by_css_selector('.phone').text
            if phone == '+ Add phone number':
                raise Exception
        except Exception:
            phone = ''

        try:
            cost = driver.find_element_by_css_selector('.price span.text').text
        except Exception:
            cost = ''

        # go to site
        main_window = driver.window_handles[0]
        try:
            link = driver.find_element_by_css_selector('.website')
            if not link.text == '+ Add website':
                link.click()
                time.sleep(3)
                new_window = driver.window_handles[1]
                driver.switch_to.window(new_window)
                website = driver.current_url
                if website == 'about:blank':
                    raise Exception
            else:
                raise Exception
        except Exception:
            website = ''

        if website is not None:

            try:
                emails = set(get_mail(driver))
                if len(emails) == 0:
                    raise Exception
                else:
                    emails = ' '.join(emails)
            except Exception:
                emails = ''
        driver.close()
        try:
            driver.switch_to.window(main_window)
            driver.close()
        except Exception:
            pass

        lock.acquire()
        with open('result.txt', 'a') as doc:
            doc.write('{}|{}|{}|{}|{}|{}|{}\n'.format(
                name_of_cafe,
                address,
                phone,
                cost,
                website,
                url,
                emails
            ))
        lock.release()
        return
    except Exception:
        return


def write_xls():
    index = 0
    n = "HYPERLINK"

    # style
    font0 = xlwt.Font()
    font0.bold = True
    style = xlwt.XFStyle()
    style.font = font0

    doc_w = xlwt.Workbook()

    # write headers
    sheet = doc_w.add_sheet('sheet1')
    sheet_row = sheet.row(index)
    sheet_row.write(0, 'name_of_cafe', style)
    sheet_row.write(1, 'address', style)
    sheet_row.write(2, 'phone', style)
    sheet_row.write(3, 'cost', style)
    sheet_row.write(4, 'website', style)
    sheet_row.write(5, 'emails', style)
    sheet_row.write(6, 'orig_url', style)
    index += 1

    with open('result.txt', 'r') as doc:
        for string in doc:
            string = string.split('|')

            sheet_row = sheet.row(index)
            sheet_row.write(0, string[0])
            sheet_row.write(1, string[1])
            sheet_row.write(2, string[2])
            sheet_row.write(3, string[3])
            sheet_row.write(4, string[4])
            sheet_row.write(5, string[6].replace('\n', ''))
            sheet_row.write(6, string[5])

            doc_w.save('result.xls')
            index += 1


#
def init(l):  # init for multiprocessing
    global lock
    lock = l


if __name__ == '__main__':
    get_links()

    hrefs = set(get_saved_links())
    l = multiprocessing.Lock()
    pool = multiprocessing.Pool(initializer=init, initargs=(l,))
    pool.map(get_page_content, hrefs)
    pool.close()
    pool.join()
    write_xls()  # save into xls
