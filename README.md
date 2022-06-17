
# ONELINER
Oneliner is a Stand-Alone reverse shell payload creator.
## Why **Oneliner**?

In real-world Pentesting Envionment, isn't it quite hard to go to some online web sites like [pentestmonkey](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) or [revshells](https://www.revshells.com/) and then set the required options and then copy, paste and do all those stuff?

Here **Oneliner** helps, **Oneliner** creates a reverse shell payload with the desired options much faster than all the above stuff.

It does only require some arguments and your payload is ready, saving much time.


## Required Arguments

- LHOST
- Shell Type

## Optional Arguments

- PORT ```Default value - 4444```
- Encode ``` Default value - None```


## Examples -
```bash
    python3 oneliner.py 10.10.15.171 -s bash
```
```powershell
    python3 oneliner.py 10.10.15.171 -s pwsh -p 1234
```
```netcat_url_encoded
    python3 oneliner.py 10.10.15.171 -s nc -e url
```

## Contributing:
    Any body can voluntarily contribute to this project if he/she has a better idea.
    If so, please contact me on my [Insta Handle](https://www.instagram.com/sayanray385/).
