from weather import get_rain_hours

def test_get_rain_hours():
    times = ["2026-10-26T13:00","2026-10-26T14:00","2026-10-26T15:00"]
    probs = [55,45,50]
    result = get_rain_hours(times, probs, 50)
    assert result == ["13:00 55%","15:00 50%"]
