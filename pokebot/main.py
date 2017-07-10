from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import getpass

def snap(browser, tag):
	with open(tag + ".html", 'w') as htmlfile:
		htmlfile.write(browser.page_source)
	browser.save_screenshot(tag + ".png")

def main():
	# launch browser
	browser = webdriver.PhantomJS()
	browser.set_window_size(800, 600)

	# login to facebook
	browser.get("http://www.facebook.com")
	snap(browser, "1-login")
	
	email, password = get_login()
	username_box = browser.find_element_by_name("email")
	username_box.send_keys(email)

	password_box = browser.find_element_by_name("pass")
	password_box.send_keys(password)

	login_button = browser.find_element_by_name("login")
	login_button.click()
	print("logging in...")
	time.sleep(2)
	print("logged in!")
	snap(browser, "2-logged-in")
	
	# okay, now go to the poke page
	browser.get("http://www.facebook.com/pokes")
	snap(browser, "3-pokes")

	# input("")

	# respond to all pokes
	poke_area = browser.find_element_by_id("contentArea")
	all_pokes = poke_area.find_elements_by_xpath("./div/div/div/div")
	pokes = [e for e in all_pokes if 'poke_live_item' in e.get_attribute('id')]

	for poke in pokes:
		person = poke.find_element_by_xpath("./div/div/div/div/div/div/a").text
		poke_button = poke.find_element_by_partial_link_text("Poke back")
		poke_button.click()
		print("poking {}".format(person))
	
	time.sleep(0.5)

	browser.quit()


	# log in to facebook

	# go to the poke page

	# if julian has poked me
		# poke him back

	# else
		# wait a while

def get_login():
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