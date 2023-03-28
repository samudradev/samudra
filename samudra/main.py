from samudra.conf.setup import bind_proxy_to_database


def start_app() -> None:
    bind_proxy_to_active_databse()


if __name__ == "__main__":
    print(
        "The current codebase is written as a library. Please do not run this as a script."
    )
