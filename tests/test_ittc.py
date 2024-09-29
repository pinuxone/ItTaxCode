from src.ittaxcode import ittc as cf


def test():
    assert cf.check(
        "PPPNNNLMBMQLMMTA"
    )

    assert cf.age(
        "PPPNNNLMBMQLMMTA"
    ) == 23

    assert str(cf.birthdate(
        "PPPNNNLMBMQLMMTA"
    )) == "2001-02-14"
