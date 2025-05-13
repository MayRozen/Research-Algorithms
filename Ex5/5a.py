# Put your iterator/generator here.
# It should be called: sorted_subset_sums.
from heapq import heappush, heappop
from typing import Iterable, Iterator, List, Tuple
from itertools import takewhile, islice


def sorted_subset_sums(seq: Iterable[int]) -> Iterator[int]:
    # הוספתי בדיקות נוספות על ידי GPT:
    # https://chatgpt.com/share/6821c7a9-5ab8-8005-b957-0c2a0e9cc3e8
    """
        Generates the sorted subset sums of the given sequence of integers.

        >>> list(sorted_subset_sums([1, 2, 3]))
        [0, 1, 2, 3, 3, 4, 5, 6]

        >>> list(sorted_subset_sums([1, 2, 4]))
        [0, 1, 2, 3, 4, 5, 6, 7]

        >>> list(sorted_subset_sums([0, 0, 0]))
        [0, 0, 0, 0, 0, 0, 0, 0]

        >>> list(sorted_subset_sums([]))
        [0]
    """
    sorted_numbers = sorted(seq)  # מיון האיברים
    num_zeros = 0  # אתחול משתנה שיתעד את כמות האפסים ברשימה
    for i in range(len(sorted_numbers)):  # חיפוש באיברי הרשימה הממוינת
        if sorted_numbers[i] != 0:  # אם נמצא איבר שאינו אפס, יוצאים מהלולאה
            break
        num_zeros += 1  # ספירת כמות האפסים

    positive_numbers: List[int] = sorted_numbers[num_zeros:]  # מיון האיברים מאחרי כל האפסים ברשימה

    # קבע כמה פעמים יש לשכפל כל סכום תת-קבוצה עקב אפסים
    duplicate_factor = 1 << num_zeros  # 2**num_zeros

    # 0 עבור כל צירוף אפסים
    for _ in range(duplicate_factor):
        yield 0

    # אם אין ערכים חיובים נצא מהפונקציה או שכל הערכים הם אפס
    if not positive_numbers or num_zeros == len(sorted_numbers):
        return

    # צור ערימה כדי לנהל את סכומי תת-הקבוצה בסדר ממוין
    num_elements = len(positive_numbers)  # כמות המספרים החיוביים
    min_heap: List[Tuple[int, int]] = [(positive_numbers[0], 0)]  # (sum, index) התחלת הקבוצה עם האיבר הראשון

    while min_heap:  # כל עוד יש איברים בheap
        current_sum, index = heappop(min_heap)
        for _ in range(duplicate_factor):  # סכומים כפולים בגלל אפסים
            yield current_sum
        if index + 1 < num_elements:
            # חישוב תת-קבוצה חדשה על ידי הסרת הערך הקודם והוספת הערך הבא
            new_sum_1 = current_sum - positive_numbers[index] + positive_numbers[index + 1]

            # חישוב תת-קבוצה חדשה על ידי הוספת הערך הבא (בלי להסיר שום ערך קודם)
            new_sum_2 = current_sum + positive_numbers[index + 1]

            # הוספת תתי-קבוצות חדשות להערימה
            heappush(min_heap, (new_sum_1, index + 1))
            heappush(min_heap, (new_sum_2, index + 1))


if __name__ == '__main__':
    for i in eval(input()):
        print(i, end=", ")

    import doctest

    doctest.testmod()
