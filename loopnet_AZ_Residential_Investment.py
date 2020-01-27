from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import re
import time

driver = webdriver.Chrome()

# open following link in the chrome browser
#driver.get("https://www.loopnet.com/arizona-commercial-real-estate/")
driver.get("https://www.loopnet.com/arizona_residential-income-properties-for-sale/")

#open csv file in the write mode
csv_file = open('arizona-residential-real-estate.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

index = 1
while index<=20:
	try:
		print("Scraping Page number " + str(index))
		index = index + 1

		# wait for all web elements to be loaded
		wait_review = WebDriverWait(driver, 10)
		time.sleep(0.5)

		# wait for all elements to loaded from the main container

		reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"listingContainer clearfix placard-view-trigger tier")]'))) 
		#driver.find_elements_by_xpath('//div[contains(@class,"listingContainer clearfix placard-view-trigger tier")]')

		for review in reviews:
			# Initialize an empty dictionary for each review
			review_dict = {}

			# Use relative xpath to locate elements
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			try:

				title=review.find_element_by_xpath('.//span[@class="listingTitle"]').text
				address = review.find_element_by_xpath('.//div[@class="listingDescription"]/a').get_attribute('title')
				location = review.find_element_by_xpath('.//div[@class="listingDescription"]/b').text
				page_link=review.find_element_by_xpath('.//div[@class="listingDescription"]/a').get_attribute('href')
				status=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Status")]/following-sibling::*').text
				price=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Price")]/following-sibling::*').text
				element=review.find_element_by_xpath('.//div[@class="listingDescription"]/a')

			except:
				continue

			try:
				prop_descr = review.find_element_by_xpath('.//span[@class="propertyDescription"]').text
			except:
				prop_descr=None

			try:
				prop_type=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Property Type")]/following-sibling::*').text
			except:
				prop_type=None

			try:
			 	prop_sub_type=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Sub-Type")]/following-sibling::*').text
			except:
				prop_sub_type=None
			
			try:
			 	spaces=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Spaces")]/following-sibling::*').text
			except:
			 	spaces=None

			try:
			 	spaces_avail=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Space Available")]/following-sibling::*').text
			except:
				spaces_avail=None

			try:
				build_size=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Building Size")]/following-sibling::*').text
			except:
				build_size=None

			try:
			 	cap_rate=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Cap Rate")]/following-sibling::*').text
			except:
			 	cap_rate=None

			try:
			  	build_class=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Building Class")]/following-sibling::*').text
			except:
			 	build_class=None

			try:
			  	lot_size=review.find_element_by_xpath('.//*[@class="listingAttributes"]/tbody/*/td[contains(text(),"Lot Size")]/following-sibling::*').text
			except:
			 	lot_size=None


			#driver.execute_script("arguments[0].scrollIntoView();", review)

			# populate values of the keys in the dictionary for each element at a time
			review_dict['title'] = title
			review_dict['address'] = address
			review_dict['location']=location
			review_dict['page_link'] = page_link
			review_dict['prop_descr'] = prop_descr
			review_dict['status']=status
			review_dict['price']=price
			review_dict['prop_type']=prop_type
			review_dict['prop_sub_type']=prop_sub_type
			review_dict['spaces']=spaces
			review_dict['spaces_avail']=spaces_avail
			review_dict['build_size']=build_size
			review_dict['cap_rate']=cap_rate
			review_dict['build_class']=build_class
			review_dict['lot_size']=lot_size

			

			
			try:

				# element=review.find_element_by_xpath('.//div[@class="listingDescription"]/a')
				#("//div[@class='listingDescription']//a/@href").extract()

				# click on the individual listing to open a new page of its detailed information
				element.send_keys(Keys.COMMAND + Keys.RETURN)
				driver.switch_to.window(driver.window_handles[1])

				#print("Scraping listing details of on page " + str(index))


				# wait for all elements to be loaded
				wait_listing = WebDriverWait(driver, 10)
				time.sleep(2)
				#print("details page opened")

				listing = wait_listing.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"column-08 column-ex-large-09 column-large-09 column-medium-09 profile-main-info")]')))
				#print("all elements loaded")

				# start capturing detailed information of the listing
				try:
					rent_rate=driver.find_element_by_xpath('//*[@class="property-data featured-grid"]/tbody/*/td[contains(text(),"Rental Rate")]/following-sibling::*').text
				except:
				 	rent_rate=None
				try:
					year_built=driver.find_element_by_xpath('//*[@class="property-data featured-grid"]/tbody/*/td[contains(text(),"Year Built")]/following-sibling::*').text
				except:
					year_built=None
				try:
					parking=driver.find_element_by_xpath('//*[@class="property-data featured-grid"]/tbody/*/td[contains(text(),"Parking Ratio")]/following-sibling::*').text
				except:
					parking=None
				try:
					occ_rate=driver.find_element_by_xpath('//*[@class="property-data featured-grid"]/tbody/*/td[contains(text(),"Average Occupancy")]/following-sibling::*').text
				except:
					occ_rate=None
				try:
					num_str=driver.find_element_by_xpath('//*[@class="property-data featured-grid"]/tbody/*/td[contains(text(),"No. Stories")]/following-sibling::*').text
				except:
					num_str=None	
				try:
					sale_status=driver.find_element_by_xpath('//span[@class="title-pill title-pill--yellow"]').text
				except:
					sale_status=None
				try:
					zoning=driver.find_element_by_xpath('//td[contains(text(),"Zoning Code")]/following-sibling::*').text
				except:
					zoning=None
				try:
					list_date=driver.find_element_by_xpath('.//ul[@class="property-timestamp"]/li[2]').text
				except:
					list_date=None
				try:
					invest_descr=driver.find_element_by_xpath('//div[@class="column-12 sales-notes-text"]/following::*').text
				except:
					invest_descr=None
				try:
					walk_score = driver.find_elements_by_xpath('//div[contains(text(),"Walk Score")]/following-sibling::*')[0].text
				except:
					walk_score=None
				try:                                         
					transit_score = driver.find_elements_by_xpath('//div[contains(text(),"Transit")]/following-sibling::*')[0].text
				except:
					transit_score=None
				try:                                         
					bike_score = driver.find_elements_by_xpath('//div[contains(text(),"Bike")]/following-sibling::*')[0].text
				except:
					bike_score=None
					#len(listing_detail.find_elements_by_xpath('//table[@class="property-data summary cols-4"]/tbody[@class="poi__content"]/tr'))/2  -- count of restaurents
					#len(listing_detail.find_elements_by_xpath('//table[@class="property-data summary cols-3"]/tbody[@class="poi__content"]/tr'))/2  -- count of retail

				# populate the dictionary with values
				review_dict['rent_rate'] = rent_rate
				review_dict['year_built'] = year_built
				review_dict['parking']=parking
				review_dict['occ_rate'] = occ_rate
				review_dict['num_str'] = num_str
				review_dict['sale_status'] = sale_status
				review_dict['zoning']=zoning
				review_dict['list_date']=list_date
				review_dict['invest_descr']=invest_descr
				review_dict['transit_score']=transit_score
				review_dict['walk_score']=walk_score
				review_dict['bike_score']=bike_score

				# write to csv file
				writer.writerow(review_dict.values())

				# print(rent_rate)
				# print(year_built)
				# print(parking)
				# print(occ_rate)
				# print(sale_status)
				# print(zoning)
				# print(list_date)
				# print(invest_descr)
				# print(transit_score)

				# close the detailed information page
				driver.close()
				#print("detailed page closed")
				
				#switch focus to main page
				driver.switch_to.window(driver.window_handles[0])
				#print("focus back")

			except Exception as e:
				print(e)
				print("something is broken")
				break

		# We need to scroll to the bottom of the page because the button is not in the current view yet.
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Locate the next button on the page.
		wait_button = WebDriverWait(driver, 10)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'//a[@class="button tiny primary caret-right"]')))
		next_button.click()

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break

#csv_file.close()
#driver.close()
