import gifts
import voyage
import utils
import themes
import hospitality

print("Downloading files...")
utils.download_csv_file("voyage")
utils.download_csv_file("hopitality")
utils.download_csv_file("gifts")
utils.download_csv_file("themes")

gifts.compile_all()
themes.compile_all()
hospitality.compile_all()
voyage.compile_all()
