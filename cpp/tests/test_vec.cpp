#include "vec.h"
#include <gtest/gtest.h>

TEST(testVec3, default_construct)
{
    Vec3<int> v;
    EXPECT_EQ(0, v.x);
    EXPECT_EQ(0, v.y);
    EXPECT_EQ(0, v.z);
}
