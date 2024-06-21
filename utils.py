def clean_raw_name(val):
    # take the string and remove all spaces, make it all upper
    # then remove all , _ and '
    return (
        val.upper().replace(" ", "").replace(",", "").replace("_", "").replace("'", "")
    )
