def shift(a, b, index):
    parts = []
    headA, headB = (a >> index) << index, (b >> index) << index
    bodyA, bodyB = a ^ headA, b ^ headB
    A, B = headA | bodyB, headB | bodyA
    parts.append((formBit(a, 10) , formBit(b, 10)))
    parts.append((formBit(headA, 10), formBit(headB, 10)))
    parts.append((formBit(bodyA, 10), formBit(bodyB, 10)))
    parts.append((formBit(A, 10), formBit(B, 10)))
    for i in parts:
        print i

def formBit(num, place):
    form = '0' + str(place) + 'b'
    return format(num, form)
