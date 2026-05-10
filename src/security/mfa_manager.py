def weighted_mfa(face: bool, voice: bool, device: bool, pin: bool) -> bool:
    """MFA pondéré : valide si le score atteint le seuil."""
    score = 0

    score += 3 if face else 0
    score += 2 if voice else 0
    score += 2 if device else 0
    score += 1 if pin else 0

    return score >= 5
