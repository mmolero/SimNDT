def sourceVel(Vx, Vy, XL, YL, source, Stype, win, dtdxx):
    if Stype == 0:
        Vx[XL[:], YL[:]] -= source * dtdxx * win[:]

    elif Stype == 1:
        Vy[XL[:], YL[:]] -= source * dtdxx * win[:]

    elif Stype == 2:
        Vx[XL[:], YL[:]] -= source * dtdxx * win[:]
        Vy[XL[:], YL[:]] -= source * dtdxx * win[:]

    return (Vx, Vy)


def sourceStress(Txx, Tyy, XL, YL, source, Stype, win, dtdxx):
    if Stype == 0:
        Txx[XL[:], YL[:]] -= source * dtdxx * win[:]

    elif Stype == 1:
        Tyy[XL[:], YL[:]] -= source * dtdxx * win[:]

    elif Stype == 2:
        Txx[XL[:], YL[:]] -= source * dtdxx * win[:]
        Tyy[XL[:], YL[:]] -= source * dtdxx * win[:]

    return (Txx, Tyy)


def velocityVoigt(Txx, Txy, Tyy, vx, vy, d_vx, d_vy, BX, BY, ABS, ddx, dt):
    d_vx[:-1, 1:] = (ddx * BX[:-1, 1:]) * (Txx[1:, 1:] - Txx[:-1, 1:] + Txy[:-1, 1:] - Txy[:-1, 0:-1]);
    vx[:-1, 1:] += dt * d_vx[:-1, 1:]

    d_vy[1:, :-1] = (ddx * BY[1:, :-1]) * (Txy[1:, :-1] - Txy[0:-1, :-1] + Tyy[1:, 1:] - Tyy[1:, :-1]);
    vy[1:, :-1] += dt * d_vy[1:, :-1]

    vx[:, :] *= ABS[:, :]
    vy[:, :] *= ABS[:, :]

    return (vx, vy, d_vx, d_vy)


def stressVoigt(Txx, Txy, Tyy, vx, vy, d_vx, d_vy, C11, C12, C44, ETA_VS, ETA_S, ETA_SS, ABS, dtx):
    Txx[1:, 1:] += ((dtx * C11[1:, 1:]) * (vx[1:, 1:] - vx[0:-1, 1:]) +
                    (dtx * C12[1:, 1:]) * (vy[1:, 1:] - vy[1:, 0:-1]) +
                    (dtx * ETA_VS[1:, 1:]) * (d_vx[1:, 1:] - d_vx[0:-1, 1:]) +
                    (dtx * ETA_S[1:, 1:]) * (d_vy[1:, 1:] - d_vy[1:, 0:-1]))

    Tyy[1:, 1:] += ((dtx * C12[1:, 1:]) * (vx[1:, 1:] - vx[0:-1, 1:]) +
                    (dtx * C11[1:, 1:]) * (vy[1:, 1:] - vy[1:, 0:-1]) +
                    (dtx * ETA_S[1:, 1:]) * (d_vx[1:, 1:] - d_vx[0:-1, 1:]) +
                    (dtx * ETA_VS[1:, 1:]) * (d_vy[1:, 1:] - d_vy[1:, 0:-1]))

    Txy[:-1, :-1] += ((dtx * C44[:-1, :-1]) * (vx[:-1, 1:] - vx[:-1, :-1] + vy[1:, :-1] - vy[:-1, :-1]) +
                      (dtx * ETA_SS[:-1, :-1]) * (d_vx[:-1, 1:] - d_vx[:-1, :-1] + d_vy[1:, :-1] - d_vy[:-1, :-1]))

    Txx[:, :] *= ABS[:, :]
    Tyy[:, :] *= ABS[:, :]
    Txy[:, :] *= ABS[:, :]

    return (Txx, Tyy, Txy)
