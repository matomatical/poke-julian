from selenium import webdriver
import time, getpass

def snap(browser, tag):
    """log the state of browser to tag.html and tag.png"""
    with open(tag + ".html", 'w') as htmlfile:
        htmlfile.write(browser.page_source)
    browser.save_screenshot(tag + ".png")

def main():
    # launch browser
    browser = webdriver.PhantomJS()
    browser.set_window_size(800, 600)

    # login to facebook
    browser.get("http://www.facebook.com")
    # snap(browser, "1-login")
    email, password = get_login()


    print("logging in...")
    browser.find_element_by_name("email").send_keys(email)
    browser.find_element_by_name("pass").send_keys(password)
    browser.find_element_by_name("login").click()
    time.sleep(2)
    print("logged in!") # hopefully that worked...
    # snap(browser, "2-logged-in")
    

    # okay, now go to the poke page
    browser.get("http://www.facebook.com/pokes")
    # snap(browser, "3-pokes")


    # repeatedly poke julian
    while True:
        
        # find all pokes
        poke_area = browser.find_element_by_id("contentArea")
        all_pokes = poke_area.find_elements_by_xpath("./div/div/div/div")
        pokes = [e for e in all_pokes if 'poke_live_item' in e.get_attribute('id')]

        julian = None
        for poke in pokes:
            person = poke.find_element_by_xpath("./div/div/div/div/div/div/a").text
            if person == "Julian Tran":
                buttons = poke.find_elements_by_partial_link_text("Poke back")
                if buttons:
                    julian = buttons[0]
                break

        # did we find julian?
        if julian:
            # yes, poke him back
            julian.click()
            print("poke!")
            time.sleep(7)

        else:
            # no, wait a while and then refresh the page
            time.sleep(30)
            browser.refresh()
            print("refreshing...")

    browser.quit()

    
def get_login():
    """get login credentials from a file, or from the user if file is missing"""
    try:
        file = open("login.txt", 'r')
        email    = file.readline().strip()
        password = file.readline().strip()
        file.close()
    except FileNotFoundError:
        email    = input("email address: ")
        password = getpass.getpass("password: ")
    return email, password


if __name__ == '__main__':
    main()