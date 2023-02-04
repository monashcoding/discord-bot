

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

# mac-discord-bot

The in-house discord bot, designed by the Monash Association of Coding (MAC). It can give information on unit requisites.


## Acknowledgements

 - [Partially inspired CSESoc's discord bot](https://github.com/csesoc/discord-bot)
 - The past MAC committee, especially Sid for assisting with scraping information
## Contributing

Contributions are always welcome! Create an issue, with a pull request if you have an addition, bug fix or something else.


## Installation

Feel free to set up a virtual environment, or otherwise. Then install the required requisites:

```bash
pip install - requirements.txt
```
    
## Environment Variables

To run this project, you will need to add a Discord application token to your `.env` file.

`token=....`

Note that this token requires the `bot` scope, in addition to general message reading permissions when inviting it. Additionally, grant it all three types of privileged gateway intents.


## Run Locally

After installing the required libraries and inserting your token, simply run the `bot.py` file, and invite it as needed.
## Roadmap

- Add Specialisations for querying

- Add Courses for querying

- Add job search functionality from certain companies

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@mtshin123](https://www.github.com/mtshin123): Primary contributor
- [@saikumarmk](https://www.github.com/saikumarmk): Secondary contributor



## Appendix

Any additional information goes here

