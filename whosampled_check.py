"""WhoSampled Submission Checker

This script checks a given user profile on the website WhoSampled for 
broken sample submissions. A sample submission can be considered 
"broken" when either of the following conditions are met:

- The YouTube videos for the sampling song and/or the original song
  won't load
- The YouTube videos for the sampling song and/or the original song
  have been replaced with widgets/players from other services
  (Spotify, SoundCloud, Bandcamp, etc.)

TODO: The second condition should be accounted for separately in the future.

Author: Joe C.
"""

from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
import undetected_chromedriver as uc
import argparse
import time


def create_soup(driver: uc.Chrome, url: str) -> BeautifulSoup:

    # Will return this empty soup if the request for the URL fails
    soup = BeautifulSoup('', 'html.parser')

    driver.get(url)

    if driver.page_source:
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    return soup


def quit_web_driver(driver: uc.Chrome):
    print("Shutting down web driver...")
    driver.quit()


def print_error(error: str):
    print(f"\n[ERROR] {error}\n")


def main():

    version = "1.0.0"
    print(f"WhoSampled Submission Checker, v{version}\n")

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help="WhoSampled "
                        "user whose profile will be parsed by this script")
    parser.add_argument('--file-output', help="Output any "
                        "broken links found to a file rather than the "
                        "terminal", action="store_true")
    args = parser.parse_args()

    if args.u is None:
        user = input("Please provide a WhoSampled user with a profile "
                     "to parse: ")
    else:
        user = args.u

    base_url = "https://www.whosampled.com"
    url = f"{base_url}/user/{user}"

    print("Initializing web driver...")

    # Check for chrome install
    try:
        driver = uc.Chrome()  # Note: Does NOT work in headless mode
        driver.minimize_window()
    except TypeError:
        print_error("Google Chrome is not installed! Exiting in error...")
        exit(1)

    print("Retrieving and parsing profile...")

    soup = create_soup(driver, url)

    # Make sure WhoSampled user provided is valid
    page_not_found_tag = soup.find('img', src="/static/images"
                                              "/redesign/misc/404.png")
    if page_not_found_tag:
        print_error(f"The following WhoSampled username is not valid: {user}")
        print("Exiting in error...")
        quit_web_driver(driver)
        exit(2)

    # Account for the case of more than one page of links
    pagination_tag = soup.find('div', class_='pagination-wrapper')

    if pagination_tag:
        pages = pagination_tag.find_all('span', class_='page')
        num_pages = max([int(p.get_text()) for p in pages])
    else:
        num_pages = 1

    print(f"\nNumber of sample submission pages detected: {num_pages}\n")

    # Visit each page and gather all the sample links
    sample_links = []
    for i in range(1, num_pages+1):

        print(f"Parsing page [{i}/{num_pages}] for samples...")

        if i != 1:
            soup = create_soup(driver, f"{url}/{i}/")

        sample_links.extend([link['href'] for link in soup.find_all('a')
                            if 'sample' in link.get_text()])

    print("\nProfile parsing complete. Number of sample submissions found:"
          f" {len(sample_links)}\n")

    broken_embed_urls = []

    for link in tqdm(sample_links):
        full_url = base_url + link

        # Parse the page contents
        sample_page = create_soup(driver, full_url)

        # Get youtube video IDs embedded on page
        yt_vid_ids = [matching_divs['data-id'] for matching_divs in
                      sample_page.find_all('div', class_=[
                          'embed-placeholder', 'youtube-placeholder'])]

        # If there are less than two YouTube embed class elements,
        # add the url to the list of pages with broken links
        if len(yt_vid_ids) != 2:
            broken_embed_urls.append(full_url)

    if broken_embed_urls:
        if args.file_output:
            timestamp = str(int(time.time()))

            output_file_path = Path.home() / f"broken_embeds_{timestamp}.txt"

            with open(output_file_path, 'w') as f:
                for broken_url in broken_embed_urls:
                    f.write(f"{broken_url}\n")

            print("\nSample submission pages with broken video embed links "
                  "have been written to the following file: ")
            print(output_file_path)
            print()

        else:
            print("\nThe following sample submission pages have broken video "
                  "embed links:")

            for broken_url in broken_embed_urls:
                print(broken_url)
            print()

        print("Work complete.\n")
    else:
        print("\nVideo embed links are valid on all scanned submission "
              "pages! Nothing to do.\n")

    quit_web_driver(driver)

    print("Exiting...")


if __name__ == '__main__':
    main()
