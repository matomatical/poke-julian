from selenium import webdriver
import time, getpass

def main():
    """Log into facebook, go to the pokes page, and repeatedly poke Julian"""

    # launch browser
    browser = webdriver.PhantomJS()
    browser.set_window_size(800, 600)

    # login to facebook
    browser.get("http://m.facebook.com")
    email, password = get_login()

    print("logging in...")
    browser.find_element_by_name("email").send_keys(email)
    browser.find_element_by_name("pass").send_keys(password)
    browser.find_element_by_name("login").click()
    time.sleep(2)
    print("done!") # hopefully that worked...


    # okay, now go to the poke page
    browser.get("http://m.facebook.com/pokes")


    # and repeatedly poke julian
    while True:
        poke_julian = find_poke_button(browser, "Julian Tran")
        if poke_julian:
            poke_julian.click()
            print("poke!")
            # now wait a suitable time to allow a poke back before trying again
            time.sleep(7)

        else:
            # if there is no poke back, wait and then try again
            time.sleep(60)
            browser.refresh()
            print("refreshing...")

    # done!
    browser.quit()


def snap(browser, tag):
    """log the state of browser to tag.html and tag.png"""
    with open(tag + ".html", 'w') as htmlfile:
        htmlfile.write(browser.page_source)
    browser.save_screenshot(tag + ".png")


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


def find_poke_button(browser, name="Julian Tran"):
    """
    find and return a button for poking back a user (name) using browser (on
    the 'pokes' page already)
    """
    # find all outstanding pokes
    poke_area = browser.find_element_by_id("poke_area")
    all_pokes = poke_area.find_elements_by_tag_name("article")
    pokes = [e for e in all_pokes if 'poke_live' in e.get_attribute('id')]

    # find the specific poke from `name`
    target_poke_button = None
    for poke in pokes:
        parts = poke.find_elements_by_xpath("./div/div/div/div/div/div/div/a")
        if len(parts) > 1:
            person = parts[0].text # the first link contains the person's name
            button = parts[1]      # the second link is the actual button
            if person == name:
                target_poke_button = button
                break
    return target_poke_button

if __name__ == '__main__':
    main()
