// Array\Array3.cpp

#include "Array3.h"
#include "ArrayTools.h"
//#include <Services\Log.h>

// intialization of static constant member
// ---------------------------------------
template <class Type> const int CArray3<Type>::DIST_FACT = 10;

// --------------
// public methods
// --------------

// constructors
// -----------
template <class Type> CArray3<Type>::CArray3(const int p_Depth, const int p_Height, const int p_Width) :
	  CContainer3<Type>(p_Depth, p_Height, p_Width) {}

template <class Type> CArray3<Type>::CArray3(const Type* p_pSrc, const int p_Depth, const int p_Height, const int p_Width) :
		CContainer3<Type>(p_pSrc, p_Depth, p_Height, p_Width) {}

template <class Type> CArray3<Type>::CArray3(const CArray3<Type>& p_Src) :
		CContainer3<Type>(p_Src) {}

// desctructor
// ----------------------------------------------------------------------------
template <class Type> CArray3<Type>::~CArray3() { }

// Addition operators
// ----------------------------------------------------------------------------
template <class Type> CArray3<Type> CArray3<Type>::operator+(const CArray3<Type>& p_Arr)
{
	CArray3<Type> l_res;
	if(Sizeof() == p_Arr.Sizeof())
	{
		l_res = (*this);
		if(!!l_res)
			CArrayTools<Type>::Add(l_res.GetBuffer(), p_Arr.GetBuffer(), l_res.GetNbElements());
		else
			LOGERR("Cannot create result array");
	}
	else
		LOGERR("Try to add arrays of different size");
		
	return l_res;
}

// ----------------------------------------------------------------------------
template <class Type> CArray3<Type> CArray3<Type>::operator+(const Type p_Val)
{
	CArray3<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Add(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

// ----------------------------------------------------------------------------
template <class Type> const CArray3<Type>& CArray3<Type>::operator+=(const CArray3<Type>& p_Arr)
{
	if(Sizeof() == p_Arr.Sizeof())
	{
		if(!!(*this))
			CArrayTools<Type>::Add(GetBuffer(), p_Arr.GetBuffer(), GetNbElements());
		else
			LOGERR("object not allocated properly");
	}
	else
		LOGERR("Try to add arrays of different size");
	
	return *this;
}

// ----------------------------------------------------------------------------
template <class Type> const CArray3<Type>& CArray3<Type>::operator+=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Add(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Subtraction operators
// ----------------------------------------------------------------------------
template <class Type> CArray3<Type> CArray3<Type>::operator-(const CArray3<Type>& p_Arr)
{
	CArray3<Type> l_res;
	if(Sizeof() == p_Arr.Sizeof())
	{
		l_res = (*this);
		if(!!l_res)
			CArrayTools<Type>::Sub(l_res.GetBuffer(), p_Arr.GetBuffer(), l_res.GetNbElements());
		else
			LOGERR("cannot create result array");
	}
	else
		LOGERR("Try to subtract arrays of different size");

	return l_res;
}

// ----------------------------------------------------------------------------
template <class Type> CArray3<Type> CArray3<Type>::operator-(const Type p_Val)
{
	CArray3<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Sub(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

// ----------------------------------------------------------------------------
template <class Type> const CArray3<Type>& CArray3<Type>::operator-=(const CArray3<Type>& p_Arr)
{
	if(Sizeof() == p_Arr.Sizeof())
	{
		if(!!(*this))
			CArrayTools<Type>::Sub(GetBuffer(), p_Arr.GetBuffer(), GetNbElements());
		else
			LOGERR("object not allocated properly");
	}
	else
		LOGERR("Try to subtract arrays of different size");
	
	return *this;
}

// ----------------------------------------------------------------------------
template <class Type> const CArray3<Type>& CArray3<Type>::operator-=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Sub(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Multiplication operators
// ----------------------------------------------------------------------------
template <class Type> CArray3<Type> CArray3<Type>::operator*(const CArray3<Type>& p_Arr)
{
	CArray3<Type> l_res(*this);
	
	if(Sizeof() == p_Arr.Sizeof())
	{
		l_res = (*this);
		if(!!l_res)
			CArrayTools<Type>::Mult(l_res.GetBuffer(), p_Arr.GetBuffer(), l_res.GetNbElements());
		else
			LOGERR("Cannot create result array");
	}
	else
		LOGERR("Try to multiply arrays of different size");
		
	return l_res;
}

// ----------------------------------------------------------------------------
template <class Type> CArray3<Type> CArray3<Type>::operator*(const Type p_Val)
{
	CArray3<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Mult(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

// ----------------------------------------------------------------------------
template <class Type> const CArray3<Type>& CArray3<Type>::operator*=(const CArray3<Type>& p_Arr)
{
	if(Sizeof() == p_Arr.Sizeof())
	{
		if(!!(*this))
			CArrayTools<Type>::Mult(GetBuffer(), p_Arr.GetBuffer(), GetNbElements());
		else
			LOGERR("object not allocated properly");
	}
	else
		LOGERR("Try to multiply arrays of different size");

	return *this;
}

// ----------------------------------------------------------------------------
template <class Type> const CArray3<Type>& CArray3<Type>::operator*=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Mult(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Subdivision operators
// ----------------------------------------------------------------------------
template <class Type> CArray3<Type> CArray3<Type>::operator/(const CArray3<Type>& p_Arr)
{
	CArray3<Type> l_res;

	if(Sizeof() == p_Arr.Sizeof())
	{
		l_res = (*this);
		if(!!l_res)
			CArrayTools<Type>::Div(l_res.GetBuffer(), p_Arr.GetBuffer(), l_res.GetNbElements());
		else
			LOGERR("Cannot create result array");
	}
	else
		LOGERR("Try to subdivide arrays of different size");
		
	return l_res;
}

// ----------------------------------------------------------------------------
template <class Type> CArray3<Type> CArray3<Type>::operator/(const Type p_Val)
{
	CArray3<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Div(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

// ----------------------------------------------------------------------------
template <class Type> const CArray3<Type>& CArray3<Type>::operator/=(const CArray3<Type>& p_Arr)
{
	if(Sizeof() == p_Arr.Sizeof())
	{
		if(!!(*this))
			CArrayTools<Type>::Div(GetBuffer(), p_Arr.GetBuffer(), GetNbElements());
		else
			LOGERR("object not allocated properly");
	}
	else
		LOGERR("Try to subdivide arrays of different size");
	
	return *this;
}

// ----------------------------------------------------------------------------
template <class Type> const CArray3<Type>& CArray3<Type>::operator/=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Div(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// various operations
// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Abs()											
{
	CArrayTools<Type>::Abs(GetBuffer(), GetNbElements());
}

template <class Type> void CArray3<Type>::Sqrt(const Type p_IfLessZero /* = 0 */)											
{
	CArrayTools<Type>::Sqrt(GetBuffer(), GetNbElements(), p_IfLessZero);
}

template <class Type> void CArray3<Type>::Log10(const Type p_IfLessOrEqZero /* = 0 */)											
{
	CArrayTools<Type>::Log10(GetBuffer(), GetNbElements(), p_IfLessOrEqZero);
}

// conversion between types
// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<char>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<BYTE>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<short>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<WORD>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<int>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<UINT>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<long>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<DWORD>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<float>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Convert(CArray3<double>& p_Result) const
{
	if(p_Result.SetSize(m_Depth, m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// various value informations
// ----------------------------------------------------------------------------
template <class Type> Type CArray3<Type>::GetMin(const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetMin(GetBuffer(), GetNbElements(), p_NoZero);
}

// ----------------------------------------------------------------------------
template <class Type> Type CArray3<Type>::GetMinPos(int& p_PosZ, int& p_PosY, int& p_PosX) const
{
	int l_pos;
	Type l_val = CArrayTools<Type>::GetMinPos(GetBuffer(), GetNbElements(), l_pos);

	int l_dim	= m_Height*m_Width;
	p_PosZ		= l_pos/l_dim;
	l_pos		= l_pos%l_dim;
	p_PosY		= l_pos/m_Width;
	p_PosX		= l_pos%m_Width;

	return l_val;
}

// ----------------------------------------------------------------------------
template <class Type> Type CArray3<Type>::GetMax(const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetMax(GetBuffer(), GetNbElements(), p_NoZero);
}

// ----------------------------------------------------------------------------
template <class Type> Type CArray3<Type>::GetMaxPos(int& p_PosZ, int& p_PosY, int& p_PosX) const
{
	int l_pos;
	Type l_val = CArrayTools<Type>::GetMaxPos(GetBuffer(), GetNbElements(), l_pos);

	int l_dim	= m_Height*m_Width;
	p_PosZ		= l_pos/l_dim;
	l_pos		= l_pos%l_dim;
	p_PosY		= l_pos/m_Width;
	p_PosX		= l_pos%m_Width;

	return l_val;
}

// ----------------------------------------------------------------------------
template <class Type> double CArray3<Type>::GetMean() const 
{ 
	return GetSum()/GetNbElements(); 
}

// ----------------------------------------------------------------------------
template <class Type> double CArray3<Type>::GetSum() const
{
	return CArrayTools<Type>::GetSum(GetBuffer(), GetNbElements());
}

// ----------------------------------------------------------------------------
template <class Type> double CArray3<Type>::GetEnergy() const
{
	return CArrayTools<Type>::GetEnergy(GetBuffer(), GetNbElements());
}

// ----------------------------------------------------------------------------
template <class Type> double CArray3<Type>::GetEntropy() const
{
	return CArrayTools<Type>::GetEntropy(GetBuffer(), GetNbElements());
}

// ----------------------------------------------------------------------------
template <class Type> double CArray3<Type>::GetHomogeneity() const
{
	return CArrayTools<Type>::GetHomogeneity(GetBuffer(), GetNbElements());
}

// ----------------------------------------------------------------------------
template <class Type> double CArray3<Type>::GetInertia() const
{
	return CArrayTools<Type>::GetInertia(GetBuffer(), GetNbElements());
}

// various Data Processing operations
// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Threshold(const long double p_ZeroToOneThershold, 
													const ThreshModeEnum p_Mode /* = LT */)
{
	Threshold(Type(GetMax()*p_ZeroToOneThershold), p_Mode);
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Threshold(const Type p_Threshold, const ThreshModeEnum p_Mode /* = LT */)
{
	CArrayTools<Type>::Threshold(GetBuffer(), GetNbElements(), p_Threshold, p_Mode);
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Threshold(const Type p_MinThreshold, const Type p_MaxThreshold,
													const ThreshModeEnum p_MinMode /* = LT */, 
													const ThreshModeEnum p_MaxMode /* = GEQ */)
{
	Threshold(p_MinThreshold, p_MinMode);
	Threshold(p_MaxThreshold, p_MaxMode);
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Binarize(const Type p_Threshold /*= 0*/, const ThreshModeEnum p_Mode /* = GT*/)
{
	CArrayTools<Type>::Binarize(GetBuffer(), GetNbElements(), p_Threshold, p_Mode);
}

// ----------------------------------------------------------------------------
template <class Type> bool CArray3<Type>::GetBinaryObjectsLimits(int& p_OffX, int& p_TailX, int& p_OffY, int& p_TailY, 
																 int& p_OffZ, int& p_TailZ)
{
	p_OffX	= m_Width;
	p_OffY	= m_Height;
	p_OffZ	= m_Depth;
	p_TailX	= -1;
	p_TailY	= -1;
	p_TailZ	= -1;

	register Type* pSrc = GetBuffer(); 
	for(register int kk=0; kk < m_Depth; kk++)
	{	for(register int jj=0; jj < m_Height; jj++)
		{	for(register int ii=0; ii < m_Width; ii++)
			{	if(*pSrc++)
				{	if(ii < p_OffX)
						p_OffX	= ii;
					if(ii > p_TailX)
						p_TailX	= ii;
					if(jj < p_OffY)
						p_OffY	= jj;
					if(jj > p_TailY)
						p_TailY	= jj;
					if(kk < p_OffZ)
						p_OffZ	= kk;
					if(kk > p_TailZ)
						p_TailZ	= kk;
	}	}	}	}

	return p_TailX != -1;
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::GetMask(CArray3<BYTE>& p_Mask) const
{
	if(p_Mask.SetSize(m_Depth, m_Height, m_Width))
	{
		p_Mask.SetValue(0);
		CArrayTools<Type>::GetMask(p_Mask.GetBuffer(), GetBuffer(), GetNbElements());
	}
	else
		LOGERR("Cannot allocate Mask array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::GetMask(CArray3<BYTE>& p_Mask, 
												  const long double p_ZeroToOneThershold,
												  const ThreshModeEnum p_Mode /* = LT */) const
{
	CArray3<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_ZeroToOneThershold, p_Mode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGERR("Cannot create intermediate array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::GetMask(CArray3<BYTE>& p_Mask, const Type p_Threshold, 
												  const ThreshModeEnum p_Mode /* = LT */) const
{
	CArray3<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_Threshold, p_Mode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGERR("Cannot create intermediate array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::GetMask(CArray3<BYTE>& p_Mask, const Type p_MinThreshold, 
												  const Type p_MaxThreshold, 
												  const ThreshModeEnum p_MinMode /* = LT */, 
												  const ThreshModeEnum p_MaxMode /* = GEQ */) const
{
	CArray3<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_MinThreshold, p_MaxThreshold, p_MinMode, p_MaxMode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGERR("Cannot create intermediate array");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Or(const CArray3<BYTE>& p_Mask)						
{
	if(m_Width == p_Mask.Width() && m_Height == p_Mask.Height() && m_Depth == p_Mask.Depth())
		CArrayTools<Type>::Or(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::And(const CArray3<BYTE>& p_Mask)						
{
	if(m_Width == p_Mask.Width() && m_Height == p_Mask.Height() && m_Depth == p_Mask.Depth())
		CArrayTools<Type>::And(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Xor(const CArray3<BYTE>& p_Mask)						
{
	if(m_Width == p_Mask.Width() && m_Height == p_Mask.Height() && m_Depth == p_Mask.Depth())
		CArrayTools<Type>::Xor(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Not()											
{
	CArrayTools<Type>::Not(GetBuffer(), GetNbElements());
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Mask(const CArray3<BYTE>& p_Mask)						
{
	if(m_Width == p_Mask.Width() && m_Height == p_Mask.Height() && m_Depth == p_Mask.Depth())
		CArrayTools<Type>::Mask(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

// margin cleaning
// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::CleanMargins(const int p_CleanWidth /* = 1 */)
{
	if(p_CleanWidth < 0)
	{
		LOGERR("Clean Width  < 0");
		return;
	}
	if(p_CleanWidth > m_Depth || p_CleanWidth > m_Height || p_CleanWidth > m_Width)
	{
		LOGERR("CleanWidth out of index range");
		return;
	}

	register int	i1, i2, jj, kk;
	int	 limZ = m_Depth - p_CleanWidth;
	int	 limY = m_Height - p_CleanWidth;
	
	for(kk=0; kk < p_CleanWidth; kk++)
		memset(&m_pData[kk][0][0], 0, m_Height*m_Width*sizeof(Type));
	
	for(; kk < limZ; kk++)
	{	for(jj=0; jj < p_CleanWidth; jj++)
			memset(&m_pData[kk][jj][0], 0, m_Width*sizeof(Type));
	
		for(; jj < limY; jj++)
		{	for(i1=0, i2=m_Width-1; i1 < p_CleanWidth; i1++, i2--)
			{	m_pData[kk][jj][i1] = 0;
				m_pData[kk][jj][i2] = 0;
		}	}
		
		for(; jj < m_Height; jj++)
			memset(&m_pData[kk][jj][0], 0, m_Width*sizeof(Type));
	}	
		
	for(; kk < m_Depth; kk++)
		memset(&m_pData[kk][0][0], 0, m_Height*m_Width*sizeof(Type));
}

// statistics operations
// ----------------------------------------------------------------------------
template <class Type> bool CArray3<Type>::Normalize()
{
	Type	sum;
		
	if((sum = Type(GetSum())) == 0)
		return false;
			
	*this	/= sum;
	
	return true;
}

// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::GetHistogram(CArray1<UINT>& p_Result) const
{
	if(p_Result.SetSize(int(GetMax()) + 1))
	{
		p_Result.SetValue(0);
		CArrayTools<Type>::GetHistogram(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	}
	else
		LOGERR("Cannot allocate result array");
}

// ----------------------------------------------------------------------------
template <class Type> bool CArray3<Type>::GetStatistics(double& p_XMean, double& p_X2Mean, double& p_XVariance, 
	const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetStatistics(GetBuffer(), GetNbElements(), p_XMean, p_X2Mean, 
				p_XVariance, p_NoZero);
}

// ----------------------------------------------------------------------------
template <class Type> double CArray3<Type>::GetCorrelation(CArray3<Type>& p_Arr) const
{
	if(!!(*this))
	{
		if(m_Width == p_Arr.Width() && m_Height == p_Arr.Height() && m_Depth == p_Arr.Depth())
			return CArrayTools<Type>::GetCorrelation(p_Arr.GetBuffer(), GetBuffer(), GetNbElements());
		else
			LOGERR("Try to compute Correlation of arrays of different size");
	}
	else
		LOGERR("object not allocated properly");

	return 0;
}

// sorting fucntion
// ----------------------------------------------------------------------------
template <class Type> void CArray3<Type>::Qsort(const bool bAscending /* = true */)
{
	CArrayTools<Type>::Qsort(GetBuffer(), GetNbElements(), bAscending);
}

// Shift elements
// --------------
template <class Type> void CArray3<Type>::Shift(const int p_OffX, const int p_OffY, const int p_OffZ)
{
	int	oXs, oYs, oZs, oXd, oYd, oZd, dimX, dimY, dimZ;
	
	if((p_OffX == 0) && (p_OffY == 0) && (p_OffZ == 0))
		return;

	if((abs(p_OffX) >= m_Width) || (abs(p_OffY) >= m_Height) || (abs(p_OffZ) >= m_Depth))
	{
		LOGERR("Offset indices out of range");
		return;
	}
		
	CArray3<Type>	dest(m_Depth, m_Height, m_Width);
	dest.SetValue(0);
	
	dimX = m_Width - abs(p_OffX);
	dimY = m_Height - abs(p_OffY);
	dimZ = m_Depth - abs(p_OffZ);
	
	if(p_OffX < 0)
	{	oXs = -p_OffX;
		oXd = 0;
	}
	else
	{	oXs = 0;
		oXd = p_OffX;
	}
	
	if(p_OffY < 0)
	{	oYs = -p_OffY;
		oYd = 0;
	}
	else
	{	oYs = 0;
		oYd = p_OffY;
	}
	
	if(p_OffZ < 0)
	{	oZs = -p_OffZ;
		oZd = 0;
	}
	else
	{	oZs = 0;
		oZd = p_OffZ;
	}

	if(!!dest)
	{
		for(int register kk=0; kk < dimZ; kk++)
			for(int register jj=0; jj < dimY; jj++)
				memcpy(&dest[oZd+kk][oYd+jj][oXd], &m_pData[oZs+kk][oYs+jj][oXs], dimX*sizeof(Type));		
		*this = dest;
	}
	else
		LOGERR("cannot create intermediate array");
}

template <class Type> void CArray3<Type>::ReflexionX()
{
	register int ii, jj, kk, i1;
	int dim = m_Width/2;
	for(kk=0; kk < m_Depth; kk++)
	{	for(jj=0; jj < m_Height; jj++)
		{	for(ii=0, i1=m_Width-1; ii < dim; ii++, i1--)
			{	Type val = m_pData[kk][jj][ii];
				m_pData[kk][jj][ii]	= m_pData[kk][jj][i1];
				m_pData[kk][jj][i1]	= val;
	}	}	}
}

template <class Type> void CArray3<Type>::ReflexionY()
{
	register int ii, jj, kk, j1;
	int dim = m_Height/2;
	for(kk=0; kk < m_Depth; kk++)
	{	for(jj=0, j1=m_Height-1; jj < dim; jj++, j1--)
		{	for(ii=0; ii < m_Width; ii++)
			{	Type val = m_pData[kk][jj][ii];
				m_pData[kk][jj][ii]	= m_pData[kk][j1][ii];
				m_pData[kk][j1][ii]	= val;
	}	}	}
}


template <class Type> void CArray3<Type>::ReflexionZ()
{
	register int ii, jj, kk, k1;
	int dim = m_Depth/2;
	for(kk=0, k1=m_Depth-1; kk < dim; kk++, k1--)
	{	for(jj=0; jj < m_Height; jj++)
		{	for(ii=0; ii < m_Width; ii++)
			{	Type val = m_pData[kk][jj][ii];
				m_pData[kk][jj][ii]	= m_pData[k1][jj][ii];
				m_pData[k1][jj][ii]	= val;
	}	}	}
}

template <class Type> void CArray3<Type>::ReflexionCenter()
{
	CArray3<Type> arr(m_Depth, m_Height, m_Width);
	
	register int ii, jj, i1, j1, kk, k1;
	if(!arr)
	{
		LOGERR("cannot create intermediate array");
		return;
	}
	for(kk=0, k1=m_Depth-1; kk < m_Depth; kk++, k1--)
		for(jj=0, j1=m_Height-1; jj < m_Height; jj++, j1--)
			for(ii=0, i1=m_Width-1; ii < m_Width; ii++, i1--)
				arr[k1][j1][i1] = m_pData[kk][jj][ii];
			
	*this = arr;
}

// manipulate isotropic volumes
// ----------------------------
template <class Type> void CArray3<Type>::GetIsotropic(CArray3<Type>& p_Result, const double p_DimPixX, const double p_DimPixZ)
{
	if(p_DimPixX == p_DimPixZ)
	{	p_Result = *this;
		return;
	}

	int	depth	= int(m_Depth*p_DimPixZ/p_DimPixX);

	while((depth-1)*p_DimPixX/p_DimPixZ >= (m_Depth-1))
		depth--;

	if(!p_Result.SetSize(depth, m_Height, m_Width))
	{
		LOGERR("Cannot allocate result array");
		return;
	}

	p_Result.SetValue(0);

	Type* pDest = p_Result.GetBuffer();
	int	dimPlane = m_Height*m_Width;
	
	for(int kk=0; kk < depth; kk++)
	{	double	zD = kk*p_DimPixX/p_DimPixZ;
		int		zI = int(zD);
		zD	-= zI;
		double	zD1 = 1 - zD;

		Type* pSrc1 = &m_pData[zI][0][0];
		Type* pSrc2 = &m_pData[zI+1][0][0];

		int dp = dimPlane;
		while(dp--)
			*pDest++ = Type(zD1**pSrc1++ + zD**pSrc2++);
	}
}

template <class Type> void CArray3<Type>::SetIsotropic(const double p_DimPixX, const double p_DimPixZ)
{
	CArray3<Type> result;

	GetIsotropic(result, p_DimPixX, p_DimPixZ);

	if(!!result)
		*this = result;
}

template <class Type> void CArray3<Type>::GetSliceX(CArray2<Type>& p_Result, const int p_PosX, const int p_PosY, 
				const int p_PosZ, const int p_ZoomFact) const
{
	if(!p_Result)
	{
		LOGERR("Result array should be allocated before the call to this function");
		return;
	}
	p_Result.SetValue(0);

	int	l_SizeI = p_Result.Width();
	int	l_SizeJ = p_Result.Height();
	int	l_HalfI = l_SizeI/(2*p_ZoomFact);
	int	l_HalfJ = l_SizeJ/(2*p_ZoomFact);
	int l_PixX	= p_PosX;
	int l_PixY	= p_PosY;
	int l_PixZ	= p_PosZ;

	if((l_PixX < 0) || (l_PixX >= m_Width))
		return;
	if((l_PixY < 0) || (l_PixY >= m_Height))
		return;
	if((l_PixZ < 0) || (l_PixZ >= m_Depth))
		return;

	int l_StartZ	= (l_PixZ - l_HalfI > 0) ? l_PixZ - l_HalfI : 0;
	int l_EndZ		= (l_PixZ + l_HalfI < m_Depth-1) ? l_PixZ + l_HalfI : m_Depth-1;
	int l_StartY	= (l_PixY - l_HalfJ > 0) ? l_PixY - l_HalfJ : 0;
	int l_EndY		= (l_PixY + l_HalfJ < m_Height-1) ? l_PixY + l_HalfJ : m_Height-1;

	for(register int zz=l_StartZ; zz<=l_EndZ; zz++)
		for(register int yy=l_StartY; yy<=l_EndY; yy++)
			for(register int jj=0, cJ=p_ZoomFact*(yy-l_PixY+l_HalfJ); (jj<p_ZoomFact)&&(cJ<l_SizeJ); jj++, cJ++)
				for(register int ii=0, cI=p_ZoomFact*(-zz+l_PixZ+l_HalfI); (ii<p_ZoomFact)&&(cI<l_SizeI); ii++, cI++)
					p_Result[cJ][cI] = m_pData[zz][yy][l_PixX];
}



template <class Type> void CArray3<Type>::GetSliceY(CArray2<Type>& p_Result, const int p_PosX, const int p_PosY, 
				const int p_PosZ, const int p_ZoomFact) const
{
	if(!p_Result)
	{
		LOGERR("Result array should be allocated before the call to this function");
		return;
	}
	p_Result.SetValue(0);

	int	l_SizeI = p_Result.Width();
	int	l_SizeJ = p_Result.Height();
	int	l_HalfI = l_SizeI/(2*p_ZoomFact);
	int	l_HalfJ = l_SizeJ/(2*p_ZoomFact);
	int l_PixX	= p_PosX;
	int l_PixY	= p_PosY;
	int l_PixZ	= p_PosZ;

	if((l_PixX < 0) || (l_PixX >= m_Width))
		return;
	if((l_PixY < 0) || (l_PixY >= m_Height))
		return;
	if((l_PixZ < 0) || (l_PixZ >= m_Depth))
		return;

	int l_StartZ	= (l_PixZ - l_HalfJ > 0) ? l_PixZ - l_HalfJ : 0;
	int l_EndZ		= (l_PixZ + l_HalfJ < m_Depth-1) ? l_PixZ + l_HalfJ : m_Depth-1;
	int l_StartX	= (l_PixX - l_HalfI > 0) ? l_PixX - l_HalfI : 0;
	int l_EndX		= (l_PixX + l_HalfI < m_Width-1) ? l_PixX + l_HalfI : m_Width-1;

	for(register int zz=l_StartZ; zz<=l_EndZ; zz++)
		for(register int xx=l_StartX; xx<=l_EndX; xx++)
			for(register int jj=0, cJ=p_ZoomFact*(-zz+l_PixZ+l_HalfJ); (jj<p_ZoomFact)&&(cJ<l_SizeJ); jj++, cJ++)
				for(register int ii=0, cI=p_ZoomFact*(xx-l_PixX+l_HalfI); (ii<p_ZoomFact)&&(cI<l_SizeI); ii++, cI++)
					p_Result[cJ][cI] = m_pData[zz][l_PixY][xx];
}


template <class Type> void CArray3<Type>::GetSliceZ(CArray2<Type>& p_Result, const int p_PosX, const int p_PosY, 
				const int p_PosZ, const int p_ZoomFact) const
{
	if(!p_Result)
	{
		LOGERR("Result array should be allocated before the call to this function");
		return;
	}
	p_Result.SetValue(0);

	int	l_SizeI = p_Result.Width();
	int	l_SizeJ = p_Result.Height();
	int	l_HalfI = l_SizeI/(2*p_ZoomFact);
	int	l_HalfJ = l_SizeJ/(2*p_ZoomFact);
	int l_PixX	= p_PosX;
	int l_PixY	= p_PosY;
	int l_PixZ	= p_PosZ;

	if((l_PixX < 0) || (l_PixX >= m_Width))
		return;
	if((l_PixY < 0) || (l_PixY >= m_Height))
		return;
	if((l_PixZ < 0) || (l_PixZ >= m_Depth))
		return;

	int l_StartY	= (l_PixY - l_HalfJ > 0) ? l_PixY - l_HalfJ : 0;
	int l_EndY		= (l_PixY + l_HalfJ < m_Height-1) ? l_PixY + l_HalfJ : m_Height-1;
	int l_StartX	= (l_PixX - l_HalfI > 0) ? l_PixX - l_HalfI : 0;
	int l_EndX		= (l_PixX + l_HalfI < m_Width-1) ? l_PixX + l_HalfI : m_Width-1;

	for(register int yy=l_StartY; yy<=l_EndY; yy++)
		for(register int xx=l_StartX; xx<=l_EndX; xx++)
			for(register int jj=0, cJ=p_ZoomFact*(yy-l_PixY+l_HalfJ); (jj<p_ZoomFact)&&(cJ<l_SizeJ); jj++, cJ++)
				for(register int ii=0, cI=p_ZoomFact*(xx-l_PixX+l_HalfI); (ii<p_ZoomFact)&&(cI<l_SizeI); ii++, cI++)
					p_Result[cJ][cI] = m_pData[l_PixZ][yy][xx];
}

template <class Type> void CArray3<Type>::GetCompress(CArray3<Type>& p_Result, const int p_ComprFact) const
{
	register int	ii, jj, kk, i1, j1, k1;
	if(p_ComprFact == 1)
	{	p_Result = *this;
		return;
	}

	int	width		= m_Width/p_ComprFact;
	int	height		= m_Height/p_ComprFact;
	int	depth		= m_Depth/p_ComprFact;
	int	fact		= p_ComprFact*p_ComprFact*p_ComprFact;
	int	incrLine	= m_Width - p_ComprFact;
	int	incrPlane	= m_Width*(m_Height - p_ComprFact);
	int	dimLine		= m_Width*p_ComprFact;
	int	dimPlane	= m_Width*m_Height*p_ComprFact;

	if(!p_Result.SetSize(depth, height, width))
	{
		LOGERR("Cannot allocate result array");
		return;
	}

	p_Result.SetValue(0);

	Type	*pDest = p_Result.GetBuffer(), *pSrcP, *pSrcL, *pSrcC, *pSrc;
	
	for(kk=0, pSrcP=GetBuffer(); kk < depth; kk++, pSrcP+=dimPlane)
	{	for(jj=0, pSrcL=pSrcP; jj < height; jj++, pSrcL+=dimLine)
		{	for(ii=0, pSrcC=pSrcL; ii < width; ii++, pSrcC+=p_ComprFact)
			{	int val = 0;
				
				for(k1=0, pSrc=pSrcC; k1 < p_ComprFact; k1++, pSrc+=incrPlane)
				{	for(j1=0; j1 < p_ComprFact; j1++, pSrc+=incrLine)
					{	for(i1=0; i1 < p_ComprFact; i1++)
						{	val += int(*pSrc++);
				}	}	}

				*pDest++	= Type(val/fact);
	}	}	}
}

template <class Type> void CArray3<Type>::SetCompress(const int p_ComprFact)
{
	CArray3<Type> result;

	GetCompress(result, p_ComprFact);

	if(!!result)
		*this = result;
}

// distance map
// ------------
template <class Type> bool	CArray3<Type>::GetDistanceMap(CArray3<short>& p_Dist, const bool p_bCityBlock /*= false*/) const
{
	if(PVOID(&p_Dist) != PVOID(this))
	{	p_Dist.SetSize(m_Depth, m_Height, m_Width);
		if(!p_Dist)
		{
			LOGERR("cannot allocate result array");
			return false;
		}
		p_Dist.SetValue(0);
	}

	const int DIST_0 = 0;
	const int DIST_0_5 = int(DIST_FACT*0.5);
	const int DIST_1_0 = int(DIST_FACT*1.0);
	const int DIST_1_4 = int(DIST_FACT*1.4);
	const int DIST_1_7 = int(DIST_FACT*1.7);
	const int DIST_2_0 = int(DIST_FACT*2.0);
	const short DIST_MIN = (SHRT_MIN + 20*DIST_2_0);
	const short DIST_MAX = (SHRT_MAX - 20*DIST_2_0);


	// initialisation	
	DistanceMapInitialize(p_Dist);

	int ii, jj, kk;
	int	limX = m_Width-1, limY = m_Height-1, limZ = m_Depth-1;
	int	dimPlane = m_Height*m_Width;
	register short* pSrc;
	register short* pDest;

	if(p_bCityBlock == true)
	{	//forward chamfering
		for(kk=1; kk < limZ; kk++)
		{	for(jj=1; jj < limY; jj++)
			{	for(ii=1, pDest=&p_Dist[kk][jj][ii]; ii < limX; ii++, pDest++)
				{	short val, val1;
					if((val = *pDest) > DIST_0_5)
					{	pSrc = pDest - 1;						
						if((val1 = *pSrc + DIST_1_0) < val)
							val = val1;

						pSrc = pDest - m_Width;
						if((val1 = *pSrc + DIST_1_0) < val)
							val = val1;

						pSrc = pDest - dimPlane;
						if((val1 = *pSrc + DIST_1_0) < val)
							val = val1;

						*pDest = val;
					}
					else if(val < -DIST_0_5)
					{	pSrc = pDest - 1;						
						if((val1 = *pSrc - DIST_1_0) > val)
							val = val1;

						pSrc = pDest - m_Width;
						if((val1 = *pSrc - DIST_1_0) > val)
							val = val1;

						pSrc = pDest - dimPlane;
						if((val1 = *pSrc - DIST_1_0) > val)
							val = val1;

						*pDest = val;
		}	}	}	}

		//backward chamfering
		for(kk=limZ-1; kk; kk--)
		{	for(jj=limY-1; jj; jj--)
			{	for(ii=limX-1, pDest=&p_Dist[kk][jj][ii]; ii; ii--, pDest--)
				{	short val, val1;
					if((val = *pDest) > DIST_0_5)
					{	pSrc = pDest + 1;						
						if((val1 = *pSrc + DIST_1_0) < val)
							val = val1;

						pSrc = pDest + m_Width;
						if((val1 = *pSrc + DIST_1_0) < val)
							val = val1;

						pSrc = pDest + dimPlane;
						if((val1 = *pSrc + DIST_1_0) < val)
							val = val1;

						*pDest = val;
					}
					else if(val < -DIST_0_5)
					{	pSrc = pDest + 1;						
						if((val1 = *pSrc - DIST_1_0) > val)
							val = val1;

						pSrc = pDest + m_Width;
						if((val1 = *pSrc - DIST_1_0) > val)
							val = val1;

						pSrc = pDest + dimPlane;
						if((val1 = *pSrc - DIST_1_0) > val)
							val = val1;

						*pDest = val;
	}	}	}	}	}
	else
	{	//forward chamfering
		for(kk=1; kk < limZ; kk++)
		{	for(jj=1; jj < limY; jj++)
			{	for(ii=1, pDest=&p_Dist[kk][jj][ii]; ii < limX; ii++, pDest++)
				{	short val, val1;
					if((val = *pDest) > DIST_0_5)
					{	pSrc = pDest - 1;						
						if((val1 = *pSrc + DIST_1_0) < val)
							val = val1;

						pSrc -= m_Width;
						if((val1 = *pSrc++ + DIST_1_4) < val)
							val = val1;
						if((val1 = *pSrc++ + DIST_1_0) < val)
							val = val1;
						if((val1 = *pSrc + DIST_1_4) < val)
							val = val1;

						pSrc -= dimPlane;
						if((val1 = *pSrc-- + DIST_1_7) < val)
							val = val1;
						if((val1 = *pSrc-- + DIST_1_4) < val)
							val = val1;
						if((val1 = *pSrc + DIST_1_7) < val)
							val = val1;

						pSrc += m_Width;
						if((val1 = *pSrc++ + DIST_1_4) < val)
							val = val1;
						if((val1 = *pSrc++ + DIST_1_0) < val)
							val = val1;
						if((val1 = *pSrc + DIST_1_4) < val)
							val = val1;
						
						pSrc += m_Width;
						if((val1 = *pSrc-- + DIST_1_7) < val)
							val = val1;
						if((val1 = *pSrc-- + DIST_1_4) < val)
							val = val1;
						if((val1 = *pSrc + DIST_1_7) < val)
							val = val1;

						*pDest = val;
					}
					else if(val < -DIST_0_5)
					{	pSrc = pDest - 1;						
						if((val1 = *pSrc - DIST_1_0) > val)
							val = val1;

						pSrc -= m_Width;
						if((val1 = *pSrc++ - DIST_1_4) > val)
							val = val1;
						if((val1 = *pSrc++ - DIST_1_0) > val)
							val = val1;
						if((val1 = *pSrc - DIST_1_4) > val)
							val = val1;

						pSrc -= dimPlane;
						if((val1 = *pSrc-- - DIST_1_7) > val)
							val = val1;
						if((val1 = *pSrc-- - DIST_1_4) > val)
							val = val1;
						if((val1 = *pSrc - DIST_1_7) > val)
							val = val1;

						pSrc += m_Width;
						if((val1 = *pSrc++ - DIST_1_4) > val)
							val = val1;
						if((val1 = *pSrc++ - DIST_1_0) > val)
							val = val1;
						if((val1 = *pSrc - DIST_1_4) > val)
							val = val1;
						
						pSrc += m_Width;
						if((val1 = *pSrc-- - DIST_1_7) > val)
							val = val1;
						if((val1 = *pSrc-- - DIST_1_4) > val)
							val = val1;
						if((val1 = *pSrc - DIST_1_7) > val)
							val = val1;

						*pDest = val;
		}	}	}	}

		//backward chamfering
		for(kk=limZ-1; kk; kk--)
		{	for(jj=limY-1; jj; jj--)
			{	for(ii=limX-1, pDest=&p_Dist[kk][jj][ii]; ii; ii--, pDest--)
				{	short val, val1;
					if((val = *pDest) > DIST_0_5)
					{	pSrc = pDest + 1;						
						if((val1 = *pSrc + DIST_1_0) < val)
							val = val1;

						pSrc += m_Width;
						if((val1 = *pSrc-- + DIST_1_4) < val)
							val = val1;
						if((val1 = *pSrc-- + DIST_1_0) < val)
							val = val1;
						if((val1 = *pSrc + DIST_1_4) < val)
							val = val1;

						pSrc += dimPlane;
						if((val1 = *pSrc++ + DIST_1_7) < val)
							val = val1;
						if((val1 = *pSrc++ + DIST_1_4) < val)
							val = val1;
						if((val1 = *pSrc + DIST_1_7) < val)
							val = val1;

						pSrc -= m_Width;
						if((val1 = *pSrc-- + DIST_1_4) < val)
							val = val1;
						if((val1 = *pSrc-- + DIST_1_0) < val)
							val = val1;
						if((val1 = *pSrc + DIST_1_4) < val)
							val = val1;
						
						pSrc -= m_Width;
						if((val1 = *pSrc++ + DIST_1_7) < val)
							val = val1;
						if((val1 = *pSrc++ + DIST_1_4) < val)
							val = val1;
						if((val1 = *pSrc + DIST_1_7) < val)
							val = val1;

						*pDest = val;
					}
					else if(val < -DIST_0_5)
					{	pSrc = pDest + 1;						
						if((val1 = *pSrc - DIST_1_0) > val)
							val = val1;

						pSrc += m_Width;
						if((val1 = *pSrc-- - DIST_1_4) > val)
							val = val1;
						if((val1 = *pSrc-- - DIST_1_0) > val)
							val = val1;
						if((val1 = *pSrc - DIST_1_4) > val)
							val = val1;

						pSrc += dimPlane;
						if((val1 = *pSrc++ - DIST_1_7) > val)
							val = val1;
						if((val1 = *pSrc++ - DIST_1_4) > val)
							val = val1;
						if((val1 = *pSrc - DIST_1_7) > val)
							val = val1;

						pSrc -= m_Width;
						if((val1 = *pSrc-- - DIST_1_4) > val)
							val = val1;
						if((val1 = *pSrc-- - DIST_1_0) > val)
							val = val1;
						if((val1 = *pSrc - DIST_1_4) > val)
							val = val1;
						
						pSrc -= m_Width;
						if((val1 = *pSrc++ - DIST_1_7) > val)
							val = val1;
						if((val1 = *pSrc++ - DIST_1_4) > val)
							val = val1;
						if((val1 = *pSrc - DIST_1_7) > val)
							val = val1;

						*pDest = val;
	}	}	}	}	}

	DistanceMapCorrection(p_Dist);

	return true;
}

// private functions called for creating a distance map
// ----------------------------------------------------
template <class Type> void CArray3<Type>::DistanceMapInitialize(CArray3<short>& p_Dist) const
{
	if(!p_Dist)
	{
		LOGERR("distance map array should already be allocated");
		return;
	}

	const int DIST_0 = 0;
	const int DIST_0_5 = int(DIST_FACT*0.5);
	const int DIST_1_0 = int(DIST_FACT*1.0);
	const int DIST_1_4 = int(DIST_FACT*1.4);
	const int DIST_1_7 = int(DIST_FACT*1.7);
	const int DIST_2_0 = int(DIST_FACT*2.0);
	const short DIST_MIN = (SHRT_MIN + 20*DIST_2_0);
	const short DIST_MAX = (SHRT_MAX - 20*DIST_2_0);

	// initialisation	
	register	Type*	pSrc = &m_pData[0][0][0];
				Type*	pLim = pSrc + m_Depth*m_Height*m_Width;
	register	short*	pDest = &p_Dist[0][0][0];

	while(pSrc != pLim)
		*pDest++ = (*pSrc++) ? DIST_MAX : DIST_MIN;

	//border correction
	int	limX = m_Width-1, limY = m_Height-1, limZ = m_Depth-1;
	int	dimPlane = m_Height*m_Width;
	register int ii, jj, kk;
	
	for(kk=1; kk < limZ; kk++)
	{	for(jj=1; jj < limY; jj++)
		{	for(ii=1, pDest=&p_Dist[kk][jj][ii]; ii < limX; ii++, pDest++)
			{	if(*pDest > 0)
				{	if(*(pDest-1) < 0)
						*pDest	= DIST_0_5;
					else if(*(pDest+1) < 0)
						*pDest	= DIST_0_5;
					else if(*(pDest-m_Width) < 0)
						*pDest	= DIST_0_5;
					else if(*(pDest+m_Width) < 0)
						*pDest	= DIST_0_5;
					else if(*(pDest-dimPlane) < 0)
						*pDest	= DIST_0_5;
					else if(*(pDest+dimPlane) < 0)
						*pDest	= DIST_0_5;
				}
				else
				{	if(*(pDest-1) > 0)
						*pDest	= -DIST_0_5;
					else if(*(pDest+1) > 0)
						*pDest	= -DIST_0_5;
					else if(*(pDest-m_Width) > 0)
						*pDest	= -DIST_0_5;
					else if(*(pDest+m_Width) > 0)
						*pDest	= -DIST_0_5;
					else if(*(pDest-dimPlane) > 0)
						*pDest	= -DIST_0_5;
					else if(*(pDest+dimPlane) > 0)
						*pDest	= -DIST_0_5;
	}	}	}	}
}

template <class Type> void CArray3<Type>::DistanceMapCorrection(CArray3<short>& p_Dist) const
{
	if(!p_Dist)
	{
		LOGERR("distance map array should already be allocated");
		return;
	}

	const int DIST_0 = 0;
	const int DIST_0_5 = int(DIST_FACT*0.5);
	const int DIST_1_0 = int(DIST_FACT*1.0);
	const int DIST_1_4 = int(DIST_FACT*1.4);
	const int DIST_1_7 = int(DIST_FACT*1.7);
	const int DIST_2_0 = int(DIST_FACT*2.0);
	const short DIST_MIN = (SHRT_MIN + 20*DIST_2_0);
	const short DIST_MAX = (SHRT_MAX - 20*DIST_2_0);

	register int ii, jj, kk;
	int	limX = m_Width-1, limY = m_Height-1, limZ = m_Depth-1;

	for(kk=1; kk < limZ; kk++)
	{	for(jj=1; jj < limY; jj++)
		{	p_Dist[kk][jj][0]		= p_Dist[kk][jj][1] - DIST_1_0;
			p_Dist[kk][jj][limX]	= p_Dist[kk][jj][limX-1] - DIST_1_0;
	}	}

	for(kk=1; kk < limZ; kk++)
	{	for(ii=0; ii < m_Width; ii++)
		{	p_Dist[kk][0][ii]		= p_Dist[kk][1][ii] - DIST_1_0;
			p_Dist[kk][limY][ii]	= p_Dist[kk][limY-1][ii] - DIST_1_0;
	}	}

	for(jj=0; jj < m_Height; jj++)
	{	for(ii=0; ii < m_Width; ii++)
		{	p_Dist[0][jj][ii]		= p_Dist[1][jj][ii] - DIST_1_0;
			p_Dist[limZ][jj][ii]	= p_Dist[limZ-1][jj][ii] - DIST_1_0;
	}	}
}

template <class Type> bool CArray3<Type>::GetObliqueSlice(CArray2<Type>& p_Result, const CPoint3D& p_Center, 
			CVector3D &p_VectX, CVector3D &p_VectY, 
			double p_VoxelSizeX , double p_VoxelSizeY , double p_VoxelSizeZ,
			double p_ZoomFact /*= 1.0*/, CSize p_Size /*= CSize(0,0)*/)
{
	if(!p_Result)
	{
		LOGERR("Result array should be allocated before the call to this function");
		return false;
	}
	p_Result.SetValue(0);

	static const bool l_IsSigned = ((Type)-1 == -1);

	int	l_ImWidth = p_Result.Width();
	int	l_ImHeight = p_Result.Height();

	if (p_Size.cx > p_Result.Width())
		p_Size.cx = p_Result.Width();
	if (p_Size.cy > p_Result.Height())
		p_Size.cy = p_Result.Height();

	double l_HalfImWidth = l_ImWidth/2.0;
	double l_HalfImHeight = l_ImHeight/2.0;

	p_VectX.Normalize();
	p_VectY.Normalize();

	int l_LimX, l_LimY, l_LimZ;
	l_LimX = Width()-1;
	l_LimY = Height()-1;
	l_LimZ = Depth()-1;

	// recherche en coord. MM du point superieur gauche de l'image dans le volume
	CPoint3D l_ImCenterMM;
	VoxelToMM(p_Center, p_VoxelSizeX, p_VoxelSizeY, p_VoxelSizeZ, l_ImCenterMM);

	double l_ImDimPixX = p_VoxelSizeX/p_ZoomFact;
	double l_ImDimPixY = p_VoxelSizeY/p_ZoomFact;
	CVector3D l_DirU(p_VectX.X()/p_ZoomFact*p_VoxelSizeX, p_VectX.Y()/p_ZoomFact*p_VoxelSizeY, 
		p_VectX.Z()/p_ZoomFact*p_VoxelSizeZ);
	CVector3D l_DirV(p_VectY.X()/p_ZoomFact*p_VoxelSizeX, p_VectY.Y()/p_ZoomFact*p_VoxelSizeY, 
		p_VectY.Z()/p_ZoomFact*p_VoxelSizeZ);

	l_DirU.Normalize();
	l_DirV.Normalize();
	
	CPoint3D l_ImOriginMM = l_ImCenterMM - l_HalfImWidth * l_ImDimPixX * l_DirU 
							- l_HalfImHeight * l_ImDimPixY * l_DirV;

	CArray1<double> l_PosX(l_ImWidth);
	CArray1<double> l_PosY(l_ImWidth);
	CArray1<double> l_PosZ(l_ImWidth);

	if(!p_Result || !l_PosX || !l_PosX || !l_PosZ)
		return false;

    for(int ii=0; ii<l_ImWidth; ii++)
    {       
        l_PosX[ii] = ii*l_ImDimPixX*l_DirU.X()/p_VoxelSizeX;
        l_PosY[ii] = ii*l_ImDimPixX*l_DirU.Y()/p_VoxelSizeY;
        l_PosZ[ii] = ii*l_ImDimPixX*l_DirU.Z()/p_VoxelSizeZ;
    }


	int l_i, l_j, l_k;
	double l_Val, l_Dx, l_Dy, l_Dz, l_Dx1, l_Dy1, l_Dz1;
	int	l_DimLine = m_Width;
	int l_DimPlane = m_Height * m_Width;

	CRect l_InterpolationRect(CPoint((l_ImWidth-p_Size.cx)/2,(l_ImHeight-p_Size.cy)/2),p_Size);

	for(register int j=0; j<l_ImHeight; j++)
	{
		double l_StartLineX = (l_ImOriginMM.X() + j*l_ImDimPixY*l_DirV.X())/p_VoxelSizeX;
		double l_StartLineY = (l_ImOriginMM.Y() + j*l_ImDimPixY*l_DirV.Y())/p_VoxelSizeY;
		double l_StartLineZ = (l_ImOriginMM.Z() + j*l_ImDimPixY*l_DirV.Z())/p_VoxelSizeZ;

		for(register int i=0; i<l_ImWidth; i++)
		{
			double l_PtX = l_StartLineX + l_PosX[i];
			double l_PtY = l_StartLineY + l_PosY[i];
			double l_PtZ = l_StartLineZ + l_PosZ[i];

			l_i = (int)l_PtX;
			l_j = (int)l_PtY;
			l_k = (int)l_PtZ;

			if(l_i>=0 && l_i<l_LimX && l_j>=0 && l_j<l_LimY && l_k>=0 && l_k<l_LimZ)
			{
				if(!l_InterpolationRect.PtInRect(CPoint(i,j)))
				{
					// pas dinterpolation
					// valeur du pixel = valeur du voxel le plus proche
					p_Result[j][i] = m_pData[l_k][l_j][l_i];
				}
				else
				{
					// mode d'interpolation tri-linéaire
					// valeur du pixel = interpolation tri-lineaire autour du voxel le plus proche
					l_Dx = l_PtX - l_i;
					l_Dy = l_PtY - l_j;
					l_Dz = l_PtZ - l_k;
					l_Dx1 = 1 - l_Dx;
					l_Dy1 = 1 - l_Dy;
					l_Dz1 = 1 - l_Dz;
					register Type* l_pSrc = &m_pData[l_k][l_j][l_i];
					l_Val =	l_Dz1*l_Dy1*l_Dx1 * *l_pSrc++;
					l_Val +=	l_Dz1*l_Dy1*l_Dx * *l_pSrc;
					l_pSrc += l_DimLine;
					l_Val +=	l_Dz1*l_Dy*l_Dx * *l_pSrc--;
					l_Val +=	l_Dz1*l_Dy*l_Dx1 * *l_pSrc;
					l_pSrc += l_DimPlane;
					l_Val +=	l_Dz*l_Dy*l_Dx1 * *l_pSrc++;
					l_Val +=	l_Dz*l_Dy*l_Dx * *l_pSrc;
					l_pSrc -= l_DimLine;
					l_Val +=	l_Dz*l_Dy1*l_Dx * *l_pSrc--;
					l_Val +=	l_Dz*l_Dy1*l_Dx1 * *l_pSrc;
					if (l_Val<0 && !l_IsSigned)
						l_Val = 0;
					p_Result[j][i] = (Type)(l_Val);
				}
			}
		}
	}
	return true;
}

// Explicit instanciation for several types
// ----------------------------------------
template class CArray3<int>;
template class CArray3<short>;
template class CArray3<BYTE>;
template class CArray3<UINT>;
template class CArray3<long>;
template class CArray3<char>;
template class CArray3<WORD>;
template class CArray3<float>;
template class CArray3<double>;
template class CArray3<DWORD>;
