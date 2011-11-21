# -*- coding: utf-8 -*-

"""
Basic thermodynamic properties in terms of (SA, t, p)

Functions:
----------
  rho_t_exact(SA, t, p)
      in-situ density
  enthalpy_t_exact(SA, t, p)
      enthalpy
  specvol_t_exact(SA, t, p)
      specific volume
  entropy_t_exact(SA, t, p)
      entropy
  cp_t_exact(SA, t, p)
      isobaric heat capacity
  Helmholtz_energy_t_exact(SA, t, p)
      Helmholtz energy
  sound_speed_t_exact(SA, t, p)
      sound speed
  pot_rho_t_exact (SA, t, p, pr=0)
      potential density
  specvol_anom_t_exact(SA, t, p)
      specific volume anomaly
  alpha_wrt_CT_t_exact (SA, t, p)
      thermal expansion coefficient with respect to Conservative Temperature.
  alpha_wrt_pt_t_exact (SA, t, p)
      thermal expansion coefficient with respect to potential temperature
  alpha_wrt_t_exact (SA, t, p)
      thermal expansion coefficient with respect to in-situ temperature
  beta_const_CT_t_exact (SA, t, p)
      saline contraction coefficient at constant Conservative Temperature.
  beta_const_pt_t_exact (SA, t, p)
      saline contraction coefficient at constant potential temperature
  beta_const_t_exact (SA, t, p)
      saline contraction coefficient at constant in-situ temperature
  internal_energy_t_exact (SA, t, p)
      internal energy
  isochoric_heat_cap_t_exact (SA, t, p)
      isochoric heat capacity
  chem_potential_relative_t_exact (SA, t, p)
      relative chemical potential
  chem_potential_water_t_exact (SA, t, p)
      chemical potential of water in seawater
  chem_potential_salt_t_exact (SA, t, p)
      chemical potential of salt in seawater
  kappa_t_exact (SA, t, p)
      isentropic compressibility
  kappa_const_t_exact (SA, t, p)
      isothermal compressibility
  adiabatic_lapse_rate_t_exact (SA, t, p)
      adiabatic lapse rate
  osmotic_coefficient_t_exact (SA, t, p)
      osmotic coefficient of seawater
  SA_from_rho_t_exact
     Absolute Salinity from density measurements

This is part of the python Gibbs Sea Water library
http://code.google.com/p/python-seawater/
"""

from __future__ import division

import numpy as np

from library import gibbs
from utilities import match_args_return, strip_mask, sfac
from constants import Kelvin, db2Pascal, P0, SSO, cp0, R
from conversion import pt_from_CT, pt_from_t, pt0_from_t, molality_from_SA

__all__ = [
           'rho_t_exact',
           'pot_rho_t_exact',
           'specvol_t_exact',
           'specvol_anom_t_exact',
           'alpha_wrt_CT_t_exact',
           'alpha_wrt_pt_t_exact',
           'alpha_wrt_t_exact',
           'beta_const_CT_t_exact',
           'beta_const_pt_t_exact',
           'beta_const_t_exact',
           'entropy_t_exact',
           'internal_energy_t_exact',
           'enthalpy_t_exact',
           'cp_t_exact',
           'isochoric_heat_cap_t_exact',
           'chem_potential_relative_t_exact',
           'chem_potential_water_t_exact',
           'chem_potential_salt_t_exact',
           'Helmholtz_energy_t_exact',
           'sound_speed_t_exact',
           'kappa_t_exact',
           'kappa_const_t_exact',
           'adiabatic_lapse_rate_t_exact',
           'SA_from_rho_t_exact',
           'osmotic_coefficient_t_exact',
          ]


@match_args_return
def Helmholtz_energy_t_exact(SA, t, p):
    r"""
    Calculates the Helmholtz energy of seawater.

    The specific Helmholtz energy of seawater :math:`f` is given by:

    .. math::
        f(SA, t, p) = g - (p + P_0) \nu = g - (p + P_0) \frac{\partial g}{\partial P}\Big|_{SA,T}

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    Helmholtz_energy : array_like
                       Helmholtz energy [J kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.Helmholtz_energy_t_exact(SA, t, p)
    array([-5985.58288209, -5830.81845224, -3806.96617841,  -877.66369421,
            -462.17033905,  -245.50407205])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 2.13.

    Modifications:
    2010-08-26. Trevor McDougall
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1
    g000 = gibbs(n0, n0, n0, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)
    return (g000 - (db2Pascal * p + P0) * g001)


@match_args_return
def rho_t_exact(SA, t, p):
    r"""
    Calculates in situ density of seawater from Absolute Salinity and in situ
    temperature.

    Parameters
    ----------
    SA : array_like
        Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    rho_t_exact : array_like
        in situ density [kg m :sup:`-3`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.rho(SA, t, p)
    array([ 1021.84017319,  1022.26268993,  1024.42771594,  1027.79020181,
            1029.83771473,  1032.00240412])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 2.8.

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall & Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1
    rho = 1. / gibbs(n0, n0, n1, SA, t, p)

    return rho


@match_args_return
def enthalpy_t_exact(SA, t, p):
    r"""
    Calculates the specific enthalpy of seawater.

    The specific enthalpy of seawater :math:`h` is given by:

    .. math::
        h(SA, t, p) = g + (T_0 + t)\eta = g - (T_0 + t) \frac{\partial g}{\partial T}\Big|_{SA,p}

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    enthalpy : array_like
               specific enthalpy [J kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.enthalpy(SA, t, p)
    array([ 115103.26047838,  114014.8036012 ,   92179.9209311 ,
             43255.32838089,   33087.21597002,   26970.5880448 ])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See appendix A.11.

    Modifications:
    2010-08-26. David Jackett, Trevor McDougall and Paul Barker.
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1
    g000 = gibbs(n0, n0, n0, SA, t, p)
    g010 = gibbs(n0, n1, n0, SA, t, p)
    return g000 - (t + Kelvin) * g010


@match_args_return
def specvol_t_exact(SA, t, p):
    r"""
    Calculates the specific volume of seawater.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    specvol : array_like
              specific volume [m :sup:`3` kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.specvol(SA, t, p)
    array([ 0.00097863,  0.00097822,  0.00097615,  0.00097296,  0.00097103,
            0.00096899])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 2.7.

    Modifications:
    2010-08-26. David Jackett & Paul Barker.
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1
    return gibbs(n0, n0, n1, SA, t, p)


@match_args_return
def entropy_t_exact(SA, t, p):
    r"""
    Calculates specific entropy of seawater.

    The specific entropy of seawater :math:`\eta` is given by:

    .. math::
        \eta(SA, t, p) = -g_T = \frac{\partial g}{\partial T}\Big|_{SA,p}

    When taking derivatives with respect to *in situ* temperature, the symbol
    :math:`T` will be used for temperature in order that these derivatives not
    be confused with time derivatives.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    entropy : array_like
              specific entropy [J kg :sup:`-1` K :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.entropy_t_exact(SA, t, p)
    array([ 400.38942528,  395.43817843,  319.8664982 ,  146.79088159,
             98.64734087,   62.79150873])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp.

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker.
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1
    return -gibbs(n0, n1, n0, SA, t, p)


@match_args_return
def cp_t_exact(SA, t, p):
    r"""
    Calculates the isobaric heat capacity of seawater.

    Parameters
    ----------
    SA : array_like
        Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    cp_t_exact : array_like
        heat capacity of seawater [J kg :sup:`-1` K :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.cp_t_exact(SA, t, p)
    array([ 4002.88800396,  4000.98028393,  3995.54646889,  3985.07676902,
            3973.59384348,  3960.18408479])

    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp.

    Modifications:
    2011-03-29. David Jackett, Trevor McDougall and Paul Barker
    """

    n0, n2 = 0, 2

    return -(t + Kelvin) * gibbs(n0, n2, n0, SA, t, p)


@match_args_return
def sound_speed_t_exact(SA, t, p):
    r"""
    Calculates the speed of sound in seawater.

    The speed of sound in seawater :math:`c` is given by:

    .. math::
        c(SA, t, p) = \sqrt{ \partial P  / \partial \rho |_{SA,\eta}} = \sqrt{(\rho\kappa)^{-1}} = g_P \sqrt{g_{TT}/(g^2_{TP} - g_{TT}g_{PP})}

    Note that in these expressions, since sound speed is in m s :sup`-1` and
    density has units of kg m :sup:`-3` it follows that the pressure of the
    partial derivatives must be in Pa and the isentropic compressibility
    :math:`kappa` must have units of Pa :sup:`-1`. The sound speed c produced
    by both the SIA and the GSW software libraries (appendices M and N) has
    units of m s :sup:`-1`.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    sound_speed : array_like
                  speed of sound in seawater [m s :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.sound_speed_t_exact(SA, t, p)
    array([ 1542.61580359,  1542.70353407,  1530.84497914,  1494.40999692,
            1487.37710252,  1483.93460908])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.17.1)

    Modifications:
    2010-07-23. David Jackett, Paul Barker and Trevor McDougall.
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1, n2 = 0, 1, 2
    g020 = gibbs(n0, n2, n0, SA, t, p)
    g011 = gibbs(n0, n1, n1, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)
    g002 = gibbs(n0, n0, n2, SA, t, p)
    return g001 * np.sqrt(g020 / (g011 ** 2 - g020 * g002))


@match_args_return
def specvol_anom_t_exact(SA, t, p):
    r"""
    Calculates specific volume anomaly from Absolute Salinity, in situ
    temperature and pressure, using the full TEOS-10 Gibbs function.

    The reference value of Absolute Salinity is SSO and the reference value of
    Conservative Temperature is equal to 0 :math:`^\circ` C.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    specvol_anom_t_exact : array_like
        specific volume anomaly  [m :sup:`3` kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.specvol_anom_t_exact(SA, t, p)
    array([  6.01044463e-06,   5.78602432e-06,   4.05564999e-06,
             1.42198662e-06,   1.04351837e-06,   7.63964850e-07])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (3.7.3)

    Modifications:
    2010-08-26. Trevor McDougall & Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1

    pt_zero = pt_from_CT(SSO, 0)

    t_zero = pt_from_t(SSO, pt_zero, 0, p)

    return  (gibbs(n0, n0, n1, SA, t, p) - gibbs(n0, n0, n1, SSO, t_zero, p))


@match_args_return
def chem_potential_relative_t_exact(SA, t, p):
    r"""
    Calculates the adiabatic lapse rate of sea water.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    chem_potential_relative : array_like
                              relative chemical potential [J kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.chem_potential_relative_t_exact(SA, t, p)
    array([ 79.4254481 ,  79.25989214,  74.69154859,  65.64063719,
            61.22685656,  57.21298557])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp.

    Modifications:
    2010-08-26. Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1
    return gibbs(n1, n0, n0, SA, t, p)


@match_args_return
def internal_energy_t_exact(SA, t, p):
    r"""
    Calculates the Helmholtz energy of seawater.

    The specific internal energy of seawater :math:`u` is given by:

    .. math::
        u(SA, t, p) = g + (T_0 + t)\eta - (p + P_0)\nu = g - (T_0 + t)\frac{\partial g}{\partial T}\Big|_{SA,p} - (p + P_0)\frac{\partial g}{\partial P}\Big|_{SA,T}

    where :math:`T_0` is the Celsius zero point, 273.15 K and
    :math:`P_0` = 101 325 Pa is the standard atmosphere pressure.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    internal_energy (u) : array_like
                          specific internal energy [J kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.internal_energy_t_exact(SA, t, p)
    array([ 114906.23847309,  113426.57417062,   90860.81858842,
             40724.34005719,   27162.66600185,   17182.50522667])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.11.1)

    Modifications:
    2010-08-22. Trevor McDougall
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1
    g000 = gibbs(n0, n0, n0, SA, t, p)
    g010 = gibbs(n0, n1, n0, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)
    return g000 - (Kelvin + t) * g010 - (db2Pascal * p + P0) * g001


@match_args_return
def kappa_const_t_exact(SA, t, p):
    r"""
    Calculates isothermal compressibility of seawater at constant in situ
    temperature.

    .. math::
        \kappa^t(SA, t, p) = \rho^{-1}\frac{\partial \rho}{\partial P}\Big|_{SA,T} = -\nu^{-1}\frac{\partial \nu}{\partial P}\Big|_{SA,T} = -\frac{g_{PP}}{g_P}

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    kappa : array_like
            Isothermal compressibility [Pa :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    This is the compressibility of seawater at constant in situ temperature.

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.kappa_const_t_exact(SA, t, p)
    array([  4.19071646e-10,   4.18743202e-10,   4.22265764e-10,
             4.37735100e-10,   4.40373818e-10,   4.41156577e-10])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.15.1)

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1, n2 = 0, 1, 2
    g002 = gibbs(n0, n0, n2, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)
    return -g002 / g001


@match_args_return
def alpha_wrt_t_exact(SA, t, p):
    r"""
    Calculates the thermal expansion coefficient of seawater with respect to in
    situ temperature.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    alpha_wrt_t : array_like
                  thermal expansion coefficient [K :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.alpha_wrt_t_exact(SA, t, p)
    array([ 0.0003256 ,  0.00032345,  0.00028141,  0.00017283,  0.00014557,
            0.00012836])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.18.1)

    .. [2] McDougall, T.J., D.R. Jackett and F.J. Millero, 2010: An algorithm
    for estimating Absolute Salinity in the global ocean. Submitted to Ocean
    Science. A preliminary version is available at Ocean Sci. Discuss.,
    6, 215-242.

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1

    g011 = gibbs(n0, n1, n1, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)
    return g011 / g001


@match_args_return
def isochoric_heat_cap_t_exact(SA, t, p):
    r"""
    Calculates the isochoric heat capacity of seawater.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    isochoric_heat_cap : array_like
                         isochoric heat capacity [J kg :sup:`-1` K :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.isochoric_heat_cap_t_exact(SA, t, p)
    array([ 3928.13708702,  3927.27381633,  3941.36418525,  3966.26126146,
            3960.50903222,  3950.13901342])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 2.21.

    Modifications:
    2010-08-26. Trevor McDougall
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1, n2 = 0, 1, 2

    g020 = gibbs(n0, n2, n0, SA, t, p)
    g011 = gibbs(n0, n1, n1, SA, t, p)
    g002 = gibbs(n0, n0, n2, SA, t, p)

    return -(Kelvin + t) * (g020 - g011 * g011 / g002)


@match_args_return
def kappa_t_exact(SA, t, p):
    r"""
    Calculates the isentropic compressibility of seawater.

    When the entropy and Absolute Salinity are held constant while the pressure
    is changed, the isentropic and isohaline compressibility
    :math:`kappa` is obtained:

    .. math::
        \kappa(SA, t, p) = \rho^{-1}\frac{\partial \rho}{\partial P}\Big|_{SA,\eta} = -\nu^{-1}\frac{\partial \nu}{\partial P}\Big|_{SA,\eta} = \rho^{-1}\frac{\partial \rho}{\partial P}\Big|_{SA,\theta} = -\nu^{-1}\frac{\partial \nu}{\partial P}\Big|_{SA,\theta} =
        -\frac{ (g_{TP}^2 - g_{TT} g_{PP} ) }{g_P g_{TT}}

    The isentropic and isohaline compressibility is sometimes called simply the
    isentropic compressibility (or sometimes the "adiabatic compressibility"),
    on the unstated understanding that there is also no transfer of salt during
    the isentropic or adiabatic change in pressure.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    kappa : array_like
            Isentropic compressibility [Pa :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    The output is Pascal and not dbar.

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.kappa_t_exact(SA, t, p)
    array([  4.11245799e-10,   4.11029072e-10,   4.16539558e-10,
             4.35668338e-10,   4.38923693e-10,   4.40037576e-10])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqns. (2.16.1) and the row for kappa in
    Table P.1 of appendix P

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1, n2 = 0, 1, 2

    g020 = gibbs(n0, n2, n0, SA, t, p)
    g011 = gibbs(n0, n1, n1, SA, t, p)
    g002 = gibbs(n0, n0, n2, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)

    return (g011 ** 2 - g020 * g002) / (g001 * g020)


@match_args_return
def SA_from_rho_t_exact(rho, t, p):
    r"""
    Calculates the Absolute Salinity of a seawater sample, for given values of
    its density, in situ temperature and sea pressure (in dbar).

    One use for this function is in the laboratory where a measured value of
    the in situ density :math:`\rho` of a seawater sample may have been made at
    the laboratory temperature :math:`t` and at atmospheric pressure :math:`p`.
    The present function will return the Absolute Salinity SA of this seawater
    sample.

    Parameters
    ----------
    rho : array_like
          in situ density [kg m :sup:`-3`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    This is expressed on the Reference-Composition Salinity Scale of
    Millero et al. (2008).

    After two iterations of a modified Newton-Raphson iteration,
    the error in SA is typically no larger than
    2 :math:`^\times` 10 :sup:`-13` [g kg :sup:`-1`]

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> rho = [1021.839, 1022.262, 1024.426, 1027.792, 1029.839, 1032.002]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.SA_from_rho_t_exact(rho, t, p)
    array([ 34.71022966,  34.89057683,  35.02332421,  34.84952096,
            34.73824809,  34.73188384])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 2.5.

    .. [2] Millero, F. J., R. Feistel, D. G. Wright, and T. J. McDougall, 2008:
    The composition of Standard Seawater and the definition of the
    Reference-Composition Salinity Scale, Deep-Sea Res. I, 55, 50-72.

    Modifications:
    2010-08-23. Trevor McDougall & Paul Barker.
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """
    n0, n1 = 0, 1
    v_lab = np.ones(rho.shape) / rho
    v_0 = gibbs(n0, n0, n1, 0, t, p)
    v_120 = gibbs(n0, n0, n1, 120, t, p)
    SA = 120 * (v_lab - v_0) / (v_120 - v_0)  # Initial estimate of SA.
    Ior = (SA < 0) | (SA > 120)
    v_SA = (v_120 - v_0) / 120  # Initial estimate of v_SA, SA derivative of v

    for k in range(0, 2):
        SA_old = SA
        delta_v = gibbs(n0, n0, n1, SA_old, t, p) - v_lab
        # Half way through the modified N-R method.
        SA = SA_old - delta_v / v_SA
        SA_mean = 0.5 * (SA + SA_old)
        v_SA = gibbs(n1, n0, n1, SA_mean, t, p)
        SA = SA_old - delta_v / v_SA

    SA[Ior] = np.ma.masked

    return SA


@match_args_return
def pot_rho_t_exact(SA, t, p, p_ref=0):
    r"""
    Calculates potential density of seawater.

    Parameters
    ----------
    SA : array_like
        Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]
    p_ref : int, float, optional
        reference pressure, default = 0

    Returns
    -------
    pot_rho : array_like
              potential density  [kg m :sup:`-3`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.pot_rho_t_exact(SA, t, p)
    array([ 1021.79814581,  1022.05248442,  1023.89358365,  1026.66762112,
            1027.10723087,  1027.40963126])
    >>> gsw.pot_rho(SA, t, p, p_ref=1000)
    array([ 1025.95554512,  1026.21306986,  1028.12563226,  1031.1204547 ,
            1031.63768355,  1032.00240412])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 3.4.

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    pt = pt_from_t(SA, t, p, p_ref=p_ref)

    return rho_t_exact(SA, pt, p_ref)


@match_args_return
def alpha_wrt_CT_t_exact(SA, t, p):
    r"""
    Calculates the thermal expansion coefficient of seawater with respect to
    Conservative Temperature.

    Parameters
    ----------
    SA : array_like
        Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    alpha_wrt_CT : array_like
                   thermal expansion coefficient [K :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.alpha_wrt_CT_t_exact(SA, t, p)
    array([ 0.00032471,  0.00032272,  0.00028118,  0.00017314,  0.00014627,
            0.00012943])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.18.3).

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1, n2 = 0, 1, 2

    pt0 = pt0_from_t(SA, t, p)

    factor = -cp0 / ((Kelvin + pt0) * gibbs(n0, n2, n0, SA, t, p))

    g011 = gibbs(n0, n1, n1, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)

    return factor * (g011 / g001)


@match_args_return
def alpha_wrt_pt_t_exact(SA, t, p):
    r"""
    Calculates the thermal expansion coefficient of seawater with respect to
    potential temperature, with a reference pressure of zero.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    alpha_wrt_pt : array_like
                   thermal expansion coefficient [K :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.alpha_wrt_pt_t_exact(SA, t, p)
    array([ 0.00032562,  0.00032355,  0.00028164,  0.00017314,  0.00014623,
            0.00012936])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.18.2).

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1, n2 = 0, 1, 2

    pt0 = pt0_from_t(SA, t, p)

    factor = gibbs(n0, n2, n0, SA, pt0, 0) / gibbs(n0, n2, n0, SA, t, p)
    g011 = gibbs(n0, n1, n1, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)

    return  factor * (g011 / g001)


@match_args_return
def beta_const_CT_t_exact(SA, t, p):
    r"""
    Calculates the saline (i.e. haline) contraction coefficient of seawater at
    constant Conservative Temperature.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    beta_const_CT : array_like
                    saline contraction coefficient [kg g :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.beta_const_CT_t_exact(SA, t, p)
    array([ 0.00071749,  0.00071765,  0.00072622,  0.00075051,  0.00075506,
            0.00075707])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.19.3)

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    # TODO: Original GSW-V3 re-implements gibbs, check what to do here!

    n0, n1, n2 = 0, 1, 2

    pt0 = pt0_from_t(SA, t, p)

    g001 = gibbs(n0, n0, n1, SA, t, p)
    g110 = gibbs(n1, n1, n0, SA, t, p)
    g100 = gibbs(n1, n0, n0, SA, pt0, 0)

    factora = g110 - g100 / (Kelvin + pt0)
    g020 = gibbs(n0, n2, n0, SA, t, p)
    factor = factora / (g001 * g020)

    g011 = gibbs(n0, n1, n1, SA, t, p)
    g101 = gibbs(n1, n0, n1, SA, t, p)

    return g011 * factor - g101 / g001


@match_args_return
def beta_const_pt_t_exact(SA, t, p):
    r"""
    Calculates the saline (i.e. haline) contraction coefficient of seawater at
    constant potential temperature with a reference pressure of 0 dbar.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    beta_const_pt : array_like
                    saline contraction coefficient [kg g :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.beta_const_pt_t_exact(SA, t, p)
    array([ 0.00073112,  0.00073106,  0.00073599,  0.00075375,  0.00075712,
            0.00075843])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.19.2)

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    # TODO: Original GSW-V3 re-implements gibbs, check what to do here!

    n0, n1, n2 = 0, 1, 2

    pt0 = pt0_from_t(SA, t, p)

    g001 = gibbs(n0, n0, n1, SA, t, p)
    g110 = gibbs(n1, n1, n0, SA, t, p)
    factora = g110 - gibbs(n1, n1, n0, SA, pt0, 0)

    g020 = gibbs(n0, n2, n0, SA, t, p)
    factor = factora / (g001 * g020)

    g011 = gibbs(n0, n1, n1, SA, t, p)
    g101 = gibbs(n1, n0, n1, SA, t, p)

    return g011 * factor - g101 / g001


@match_args_return
def beta_const_t_exact(SA, t, p):
    r"""
    Calculates the saline (i.e. haline) contraction coefficient of seawater at
    constant in situ temperature.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    beta_const_t : array_like
                   saline contraction coefficient [kg g :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.beta_const_t_exact(SA, t, p)
    array([ 0.00073112,  0.00073107,  0.00073602,  0.00075381,  0.00075726,
            0.00075865])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.19.1)

    Modifications:
    2010-07-23. David Jackett, Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1 = 0, 1

    g101 = gibbs(n1, n0, n1, SA, t, p)
    g001 = gibbs(n0, n0, n1, SA, t, p)
    return -g101 / g001


@match_args_return
def chem_potential_water_t_exact(SA, t, p):
    r"""
    Calculates the chemical potential of water in seawater.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    chem_potential_water : array_like
                           chemical potential of water in seawater
                           [J kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.chem_potential_water_t_exact(SA, t, p)
    array([-8545.56114628, -8008.08554834, -5103.98013987,  -634.06778275,
            3335.56680347,  7555.43444597])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp.

    Modifications:
    2010-09-28. Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """
    SA, t, p, mask = strip_mask(SA, t, p)

    # FIXME: Ugly copy from gibbs, why?

    x2 = sfac * SA

    x = np.sqrt(x2)
    y = t * 0.025
    z = p * 1e-4  # Pressure (p) is sea pressure in units of dbar.

    g03_g = (101.342743139674 + z * (100015.695367145 +
        z * (-2544.5765420363 + z * (284.517778446287 +
        z * (-33.3146754253611 + (4.20263108803084 -
        0.546428511471039 * z) * z)))) +
        y * (5.90578347909402 + z * (-270.983805184062 +
        z * (776.153611613101 + z * (-196.51255088122 +
        (28.9796526294175 - 2.13290083518327 * z) * z))) +
        y * (-12357.785933039 + z * (1455.0364540468 +
        z * (-756.558385769359 + z * (273.479662323528 +
        z * (-55.5604063817218 + 4.34420671917197 * z)))) +
        y * (736.741204151612 + z * (-672.50778314507 +
        z * (499.360390819152 + z * (-239.545330654412 +
        (48.8012518593872 - 1.66307106208905 * z) * z))) +
        y * (-148.185936433658 + z * (397.968445406972 +
        z * (-301.815380621876 + (152.196371733841 -
        26.3748377232802 * z) * z)) +
        y * (58.0259125842571 + z * (-194.618310617595 +
        z * (120.520654902025 + z * (-55.2723052340152 +
        6.48190668077221 * z))) +
        y * (-18.9843846514172 + y * (3.05081646487967 -
        9.63108119393062 * z) +
        z * (63.5113936641785 + z * (-22.2897317140459 +
        8.17060541818112 * z)))))))))

    g08_g = x2 * (1416.27648484197 +
        x * (-2432.14662381794 + x * (2025.80115603697 +
        y * (543.835333000098 + y * (-68.5572509204491 +
        y * (49.3667694856254 + y * (-17.1397577419788 +
        2.49697009569508 * y))) - 22.6683558512829 * z) +
        x * (-1091.66841042967 - 196.028306689776 * y +
        x * (374.60123787784 - 48.5891069025409 * x +
        36.7571622995805 * y) + 36.0284195611086 * z) +
        z * (-54.7919133532887 + (-4.08193978912261 -
        30.1755111971161 * z) * z)) +
        z * (199.459603073901 + z * (-52.2940909281335 +
        (68.0444942726459 - 3.41251932441282 * z) * z)) +
        y * (-493.407510141682 + z * (-175.292041186547 +
        (83.1923927801819 - 29.483064349429 * z) * z) +
        y * (-43.0664675978042 + z * (383.058066002476 +
        z * (-54.1917262517112 + 25.6398487389914 * z)) +
        y * (-10.0227370861875 - 460.319931801257 * z + y *
        (0.875600661808945 + 234.565187611355 * z))))) +
        y * (168.072408311545))

    g_SA_part = (8645.36753595126 +
        x * (-7296.43987145382 + x * (8103.20462414788 +
        y * (2175.341332000392 + y * (-274.2290036817964 +
        y * (197.4670779425016 + y * (-68.5590309679152 +
        9.98788038278032 * y))) - 90.6734234051316 * z) +
        x * (-5458.34205214835 - 980.14153344888 * y +
        x * (2247.60742726704 - 340.1237483177863 * x +
        220.542973797483 * y) + 180.142097805543 * z) +
        z * (-219.1676534131548 + (-16.32775915649044 -
        120.7020447884644 * z) * z)) +
        z * (598.378809221703 + z * (-156.8822727844005 +
        (204.1334828179377 - 10.23755797323846 * z) * z)) +
        y * (-1480.222530425046 + z * (-525.876123559641 +
        (249.57717834054571 - 88.449193048287 * z) * z) +
        y * (-129.1994027934126 + z * (1149.174198007428 +
        z * (-162.5751787551336 + 76.9195462169742 * z)) +
        y * (-30.0682112585625 - 1380.9597954037708 * z + y *
        (2.626801985426835 + 703.695562834065 * z))))) +
        y * (1187.3715515697959))

    chem_potential_water = g03_g + g08_g - 0.5 * sfac * SA * g_SA_part

    return np.ma.array(chem_potential_water, mask=mask, copy=False)


@match_args_return
def chem_potential_salt_t_exact(SA, t, p):
    r"""
    Calculates the chemical potential of salt in seawater.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    chem_potential_salt : array_like
        chemical potential of salt in seawater [J kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.chem_potential_salt_t_exact(SA, t, p)
    array([-8466.13569818, -7928.8256562 , -5029.28859129,  -568.42714556,
            3396.79366004,  7612.64743154])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 2.9.

    Modifications:
    2010-09-28. Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    return (chem_potential_relative_t_exact(SA, t, p) +
                                        chem_potential_water_t_exact(SA, t, p))


@match_args_return
def adiabatic_lapse_rate_t_exact(SA, t, p):
    r"""
    Calculates the adiabatic lapse rate of sea water.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    adiabatic_lapse_rate : array_like
                           Adiabatic lapse rate [K Pa :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    The output is in unit of degrees Celsius per Pa, (or equivalently K/Pa) not
    in units of K/dbar

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.adiabatic_lapse_rate_t_exact(SA, t, p)
    array([  2.40350282e-08,   2.38496700e-08,   2.03479880e-08,
             1.19586543e-08,   9.96170718e-09,   8.71747270e-09])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See Eqn. (2.22.1).

    Modifications:
    2010-08-26. Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    n0, n1, n2 = 0, 1, 2
    g011 = gibbs(n0, n1, n1, SA, t, p)
    g020 = gibbs(n0, n2, n0, SA, t, p)
    return - g011 / g020


@match_args_return
def osmotic_coefficient_t_exact(SA, t, p):
    r"""
    Calculates the osmotic coefficient of seawater.

    Parameters
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    osmotic_coefficient : array_like
                          osmotic coefficient of seawater [unitless]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.gibbs as gsw
    >>> SA = [34.7118, 34.8915, 35.0256, 34.8472, 34.7366, 34.7324]
    >>> t = [28.7856, 28.4329, 22.8103, 10.2600, 6.8863, 4.4036]
    >>> p = [10, 50, 125, 250, 600, 1000]
    >>> gsw.osmotic_coefficient_t_exact(SA,t , p)
    array([ 0.90284718,  0.90298624,  0.90238866,  0.89880927,  0.89801054,
            0.89767912])

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp.

    Modifications:
    2010-09-28. Trevor McDougall and Paul Barker
    2010-12-09. Filipe Fernandes, Python translation from gsw toolbox.
    """

    # TODO: Original GSW-V3 re-implements gibbs, check what to do here!

    n0 = 0

    # Molality of seawater in mol/kg
    molal = molality_from_SA(SA)
    part = molal * R * (Kelvin + t)

    SAzero = 0
    g000 = gibbs(n0, n0, n0, SAzero, t, p)
    return  (g000 - chem_potential_water_t_exact(SA, t, p)) / part


@match_args_return
def dynamic_enthalpy_t_exact(SA, t, p):
    r"""
    Calculates the dynamic enthalpy of seawater from Absolute Salinity, in situ
    temperature and pressure.  Dynamic enthalpy was defined by Young (2010) as
    the difference between enthalpy and potential enthalpy. Note that this
    function uses the full TEOS-10 Gibbs function (i.e. the sum of the IAPWS-09
    and IAPWS-08 Gibbs functions, see the TEOS-10 Manual, IOC et al. (2010)).

    Parameters
    ----------
    SA : array_like
        Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    p : array_like
        pressure [dbar]

    Returns
    -------
    dynamic_enthalpy_t_exact : array_like
        dynamic enthalpy [J :sup:`-1`]


    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp.

    .. [2] Young, W.R., 2010: Dynamic enthalpy, Conservative Temperature, and
    the seawater Boussinesq approximation. Journal of Physical Oceanography,
    40, 394-400.

    Modifications:
    2011-04-11. Trevor McDougall and Paul Barker
    """

    CT = CT_from_t(SA, t, p)

    return enthalpy_t_exact(SA, t, p) - cp0 * CT


@match_args_return
def t_maxdensity_exact(SA, p):
    r"""
    Calculates the in-situ temperature of maximum density of seawater. This
    function returns the in-situ temperature at which the density of seawater
    is a maximum, at given Absolute Salinity, SA, and sea pressure, p (in
    dbar).

    Parameters
    ----------
    SA : array_like
        Absolute salinity [g kg :sup:`-1`]
    p : array_like
        pressure [dbar]

    Returns
    -------
    t_maxdensity_exact : array_like
        max in-situ temperature [:math:`^\circ` C]


    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 3.42.

    Modifications:
    2011-04-03. Trevor McDougall and Paul Barker
    """

    n0, n1 = 0, 1
    # The temperature increment for calculating the gibbs_PTT derivative.
    dt = 0.001
    t = 3.978 - 0.22072 * SA  # The initial guess of t_maxden.
    gibbs_PTT = 1.1e-8  # The initial guess for g_PTT.

    for Number_of_iterations in range(0, 3):
        t_old = t
        gibbs_PT = gibbs(n0, n1, n1, SA, t_old, p)
        # This is half way through the modified method
        t = t_old - gibbs_PT / gibbs_PTT
        t_mean = 0.5 * (t + t_old)
        gibbs_PTT = (gibbs(n0, n1, n1, SA, t_mean + dt, p) -
                    gibbs(n0, n1, n1, SA, t_mean - dt, p)) / (dt + dt)
        t = t_old - gibbs_PT / gibbs_PTT

    # After three iterations of this modified Newton-Raphson iteration, the
    # error in t_maxdensity_exact is typically no larger than 1x10^-15 deg C.

    return t


@match_args_return
def osmotic_pressure_t_exact(SA, t, pw):
    r"""
    Calculates the osmotic pressure of seawater.

    Parameters
    ----------
    SA : array_like
        Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]
    pw : array_like
        sea pressure of the pure water side [dbar]

    Returns
    -------
    osmotic_pressure_t_exact : array_like
        dynamic osmotic pressure of seawater [dbar]


    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp. See section 3.41.

    Modifications:
    2011-05-26. Trevor McDougall and Paul Barker
    """

    gibbs_pure_water = gibbs(0, 0, 0, 0, t, pw)

    # Initial guess of p, in dbar.
    p = pw + 235.4684

    # Initial guess of df/dp.
    df_dp = -db2Pascal * (gibbs(0, 0, 1, SA, t, p) -
                          SA * gibbs(1, 0, 1, SA, t, p))

    for Number_of_iterations in range(0, 2):
        p_old = p
        f = gibbs_pure_water - chem_potential_water_t_exact(SA, t, p_old)
        # This is half way through the modified N-R method.
        p = p_old - f / df_dp
        p_mean = 0.5 * (p + p_old)
        df_dp = -db2Pascal * (gibbs(0, 0, 1, SA, t, p_mean) -
                              SA * gibbs(1, 0, 1, SA, t, p_mean))
        p = p_old - f / df_dp

    # After two iterations though the modified Newton-Raphson technique the
    # maximum error is 6x10^-12 dbar.

    # Osmotic pressure of seawater, in dbar.
    return p - pw


if __name__ == '__main__':
    import doctest
    doctest.testmod()
