# instawork

An assignment given by Instawork

### Prerequisites:

- [Python 3.10][python-download]

### Setup:

1. **Clone this repository**
2. **Cd into the cloned repository [the main directory]**
    ```sh
    $ cd instawork
    ```
3. **Setup your virtualenv**

   Mac:
    ```sh
    $ virtualenv venv
    $ source venv/bin/activate
    ```
   Windows:
    ```sh
    $ pip install virtualenv
    $ virtualenv --python C:\Path\To\Python\python.exe venv
    $ .\venv\Scripts\activate
    $ pip install -r requirements.txt
    ```
   Linux:
    ```sh
    $ virtualenv --python python3.6 venv
    $ source venv/bin/activate
    ```
4. **Install the required libraries**
    ```sh
    $ pip install -r requirements.txt
    ```
5. **Initialize and run the server**
    ```sh
    $ python manage.py migrate
    $ python manage.py runserver [127.0.0.1:8000]
    ```

**You are all set!**

## Tests

#### Run:

```sh
$ python manage.py test
```

#### Do you need coverage report?

```sh
$ coverage run manage.py test
$ coverage report
```

Output:

![Screen Shot 2022-07-16 at 9 18 51 PM](https://user-images.githubusercontent.com/23612067/179383820-cf910049-e5b1-40a8-931e-a6ffe8edc799.png)

[python-download]: https://www.python.org/downloads/

## Total time spent (approx.):

2.5 working days.
